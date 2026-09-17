 🌱 AgriProcureHub - Mandi Portal
> *Smarter Farming • Better Tomorrow*

 Overview
**AgriProcureHub** is a digital procurement platform designed to bridge the gap between farmers, local mandi (market) staff, and government administrators. It solves traditional agricultural bottlenecks by digitizing token queues, tracking payments transparently, broadcasting real-time center alerts, and providing a multilingual AI agri-advisor.


Key Features

 1. Farmer Portal
* **Digital Token Booking:** Farmers can easily register their crop delivery details, select their preferred time slot, and instantly receive a digital entry token with expected payouts calculated using official **MSP (Minimum Support Price)** rates.
* **Live Queue Status:** Tracks active farmers in line and dynamically estimates waiting times.
* **Payment Tracking:** Farmers can look up their token number to check their weighment status, quality grades, final payout amounts, and expected bank credit dates.
* **Multilingual AI Agri-Advisor:** Farmers can ask questions using **Voice Input** (supported by speech-to-text with auto-correction for regional farming terms) or **Text Input** in Telugu, Hindi, or English to get instant answers based on official government agricultural guidelines.

 2. Center Staff Portal
* **Bottleneck Broadcasting:** Weighbridge operators can report operational issues (such as transport delays, storage congestion, scale breakdowns, or weather alerts) which instantly trigger warning banners on the farmer portal and send emergency SMS alerts.
* **Weighbridge Inspections:** Staff can review incoming farmers, record actual weighed quantities, assign quality grades (*FAQ*, *Grade A/B*), and automatically forward payment files to the banking portal.

 3. Government Admin Portal
* **Center & Staff Management:** High-level officials can monitor the live health of all mandi centers across the state and manage staff accounts.
* **Reports & Master Ledger:** Tracks macro-level statistics including total bookings, completed procurements, and total financial liability transferred to banks.
* **SMS Gateway Logs:** Maintains a transparent, real-time audit trail of all simulated text messages sent out across the network.


 Tech Stack
* **Frontend & UI:** Streamlit (Python web framework) + Custom CSS (Inter font styling)
* **Data & State Management:** Pandas (dataframes) & Python Session State (`st.session_state` for lightning-fast in-memory storage)
* **AI & Intelligence:** Custom Python RAG pipeline (`AgriRAG`) for policy document search
* **Voice & Speech:** Streamlit Audio Recorder + OpenAI Whisper API (`whisper-large-v3`)

 Quick Start (How to Run Locally)
**Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/agriprocurehub.git](https://github.com/your-username/agriprocurehub.git)
   cd agriprocurehub
