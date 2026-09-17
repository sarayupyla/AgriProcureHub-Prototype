import os

# Create the data directory
os.makedirs("data", exist_ok=True)

# Define document contents
msp_text = """Government of India Minimum Support Price (MSP) Guidelines
Kharif and Rabi Seasons (2024-2025)

The Minimum Support Prices (MSP) for various agricultural commodities in India are announced by the government for each cropping season to guarantee farmers a minimum price. 

Kharif Crops MSP (Monsoon crops, Rs/quintal) for 2024-25:
- Paddy (Common): Rs. 2,300
- Paddy (Grade 'A'): Rs. 2,320
- Jowar (Hybrid): Rs. 3,371
- Bajra: Rs. 2,625
- Ragi: Rs. 4,290
- Maize: Rs. 2,225
- Tur (Arhar): Rs. 7,550
- Moong: Rs. 8,682
- Urad: Rs. 7,400
- Groundnut: Rs. 6,783
- Sunflower Seed: Rs. 7,280
- Soyabean: Rs. 4,892
- Sesamum: Rs. 9,267
- Cotton (Medium Staple): Rs. 7,121
- Cotton (Long Staple): Rs. 7,521
- Jute: Rs. 5,335

Rabi Crops MSP (Winter crops, Rs/quintal) for 2024-25:
- Wheat: Rs. 2,425
- Barley: Rs. 1,980
- Gram: Rs. 5,650
- Masur (Lentil): Rs. 6,700
- Rapeseed & Mustard: Rs. 5,950
- Safflower: Rs. 5,940
- Toria: Rs. 5,950

Commercial Crops (Rs/quintal) for 2024:
- Copra (Milling): Rs. 11,160
- Copra (Ball): Rs. 12,000"""

fci_text = """Food Corporation of India (FCI) Uniform Grain Specifications
Kharif Marketing Season (KMS) 2024-2025

General Condition:
Paddy shall be in sound merchantable condition, dry, clean, uniform in color and size of grains, and free from molds, weevils, obnoxious smell, Argemone mexicana, Lathyrus sativus (Khesari), and admixture of deleterious substances.

Classification:
All Paddy varieties are classified into two Grades: 'A' and 'Common', based on the length and breadth ratio (L:B). If the ratio is greater than or equal to 2.5, it is Grade 'A'. If the ratio is less than 2.5, it is 'Common'.

Maximum Permissible Limits (Refractions) for Paddy:
1. Foreign Matter (Inorganic): 1.0% maximum
2. Foreign Matter (Organic): 1.0% maximum
3. Damaged, discoloured, sprouted and weevilled grains: 5.0% maximum (Note: Damaged, sprouted, and weevilled grains alone should not exceed 4%)
4. Immature, Shrunken and shrivelled grains: 3.0% maximum
5. Admixture of lower class: 6.0% maximum
6. Moisture content: 17.0% maximum

Poisonous Seeds Limit:
Within the overall limit of 1.0% for organic foreign matter, poisonous seeds shall not exceed 0.5%, of which Dhatura and Akra seeds (Vicia species) must not exceed 0.025% and 0.2% respectively."""

mandi_text = """Government Mandi Procurement Portal - Gate Pass & Token Guidelines

Booking a Token:
Farmers must book a token through the online portal before arriving at the Mandi. The token reserves a specific time slot for bringing the harvest to the procurement center. 

Required Documents at the Gate:
Farmers must present the following documents at the Mandi gate:
1. The digital or printed Token ID.
2. Original Aadhaar Card.
3. Updated Land Records (Patta/Chitta).
4. Bank Passbook (for direct benefit transfer of MSP payments).

Queue System Rules:
- Farmers are only allowed to enter the Mandi during their designated time slot.
- The queue status on the portal shows how many farmers are currently ahead of you in your specific time slot.
- If a farmer misses their designated time slot, their token becomes invalid, and they must book a new token for the next available day.
- Crop weighing and quality inspection will occur sequentially based on the token number within that hour."""

# Write to files
files = {
    "data/msp_prices_2024_25.txt": msp_text,
    "data/fci_quality_norms_paddy.txt": fci_text,
    "data/mandi_queue_faq.txt": mandi_text
}

for filepath, content in files.items():
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
        print(f"✅ Created {filepath}")