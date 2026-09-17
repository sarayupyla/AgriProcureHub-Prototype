import os
import math
import pickle
import re
from collections import Counter
from typing import List, Any
from src.data_loader import load_documents

def tokenize(text):
    # Convert to lowercase and extract words
    return re.findall(r'\w+', text.lower())

class FaissVectorStore:
    """
    A pure Python local search index (TF-IDF) that mimics FAISS.
    It requires NO internet and avoids all Python 3.13 threading bugs!
    """
    def __init__(self, persist_dir="faiss_store"):
        self.persist_dir = persist_dir
        self.metadata = []
        self.idf = {}
        self.tf_idf_matrix = []
        os.makedirs(self.persist_dir, exist_ok=True)

    def compute_tf(self, text):
        words = tokenize(text)
        count = Counter(words)
        total = len(words)
        if total == 0: return {}
        return {w: c/total for w, c in count.items()}

    def build_from_chunks(self, chunks: List[Any]):
        print(f"[INFO] Building Local Search Index from {len(chunks)} chunks...")
        self.metadata = [{"text": c.page_content, **c.metadata} for c in chunks]
        
        # 1. Build Vocabulary and Inverse Document Frequency (IDF)
        doc_words = [set(tokenize(c.page_content)) for c in chunks]
        N = len(chunks)
        word_doc_counts = Counter()
        for words in doc_words:
            for w in words:
                word_doc_counts[w] += 1
                
        self.idf = {w: math.log((1+N)/(1+count)) + 1 for w, count in word_doc_counts.items()}
        
        # 2. Build TF-IDF matrix
        for chunk in chunks:
            tf = self.compute_tf(chunk.page_content)
            vec = {w: tf[w] * self.idf.get(w, 0) for w in tf}
            self.tf_idf_matrix.append(vec)
            
        self.save()
        print(f"[INFO] Search Index successfully saved to {self.persist_dir}")

    def save(self):
        with open(os.path.join(self.persist_dir, "index.pkl"), "wb") as f:
            pickle.dump((self.metadata, self.idf, self.tf_idf_matrix), f)

    def load(self):
        with open(os.path.join(self.persist_dir, "index.pkl"), "rb") as f:
            self.metadata, self.idf, self.tf_idf_matrix = pickle.load(f)
        print("[INFO] Search Index loaded successfully.")

    def query(self, query_text: str, top_k: int = 3):
        q_tf = self.compute_tf(query_text)
        q_vec = {w: q_tf[w] * self.idf.get(w, 0) for w in q_tf if w in self.idf}
        
        # Calculate Cosine Similarity
        def cosine_sim(vec1, vec2):
            intersection = set(vec1.keys()) & set(vec2.keys())
            dot = sum(vec1[w] * vec2[w] for w in intersection)
            mag1 = math.sqrt(sum(v**2 for v in vec1.values()))
            mag2 = math.sqrt(sum(v**2 for v in vec2.values()))
            if mag1 == 0 or mag2 == 0: return 0
            return dot / (mag1 * mag2)

        # Score all documents
        scores = [(i, cosine_sim(q_vec, doc_vec)) for i, doc_vec in enumerate(self.tf_idf_matrix)]
        scores.sort(key=lambda x: x[1], reverse=True)
        
        # Return top matches
        results = []
        for i, score in scores[:top_k]:
            if score > 0:
                results.append({"metadata": self.metadata[i], "distance": score})
        
        # Fallback if no exact keyword match is found
        if not results and self.metadata:
            results.append({"metadata": self.metadata[0], "distance": 0})
            
        return results

if __name__ == "__main__":
    chunks = load_documents()
    store = FaissVectorStore(persist_dir="faiss_store")
    store.build_from_chunks(chunks)