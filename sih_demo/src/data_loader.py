import os

class SimpleDocument:
    def __init__(self, page_content, metadata):
        self.page_content = page_content
        self.metadata = metadata

def load_documents(data_dir="data"):
    documents = []
    if not os.path.exists(data_dir):
        os.makedirs(data_dir, exist_ok=True)
        return documents
        
    for filename in os.listdir(data_dir):
        if filename.endswith(".txt"):
            file_path = os.path.join(data_dir, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
                # Simple paragraph-based chunking
                chunks = [p.strip() for p in text.split("\n\n") if p.strip()]
                for chunk in chunks:
                    documents.append(
                        SimpleDocument(
                            page_content=chunk,
                            metadata={"source": filename, "text": chunk}
                        )
                    )
                    
    print(f"Successfully loaded documents from {data_dir} into {len(documents)} chunks.")
    return documents

if __name__ == "__main__":
    load_documents()