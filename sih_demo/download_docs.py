import os
import requests

os.makedirs("data/pdf", exist_ok=True)

# Removed the broken TK Guidelines link so it runs cleanly
pdf_sources = {
    "Patents_Act_1970.pdf": "https://www.wipo.int/edocs/lexdocs/laws/en/in/in114en.pdf",
    "Biodiversity_Act_2002.pdf": "https://megbiodiversity.nic.in/sites/default/files/Biodiversity_Act_2002.pdf"
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

for filename, url in pdf_sources.items():
    filepath = os.path.join("data/pdf", filename)
    print(f"Downloading {filename}...")
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status() 
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f"✅ Saved successfully to {filepath}")
    except Exception as e:
        print(f"❌ Failed to download {filename}. Error: {e}")

print("\nFinished downloading all legal documents!")