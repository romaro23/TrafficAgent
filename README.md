# Traffic Anomaly Agent 🚦🤖

An AI-integrated backend microservice designed to automatically detect fraudulent traffic and budget anomalies in advertising campaigns. 

## 🎯 Business Value
In performance marketing and traffic arbitrage, late reaction to bot traffic or overspending can drain budgets in hours. This service processes synthetic campaign metrics (clicks, leads, revenue, cost) and flags statistical outliers. It then leverages LLM to generate clear, business-readable alerts for media buyers.

## 🛠 Tech Stack
* **Backend:** FastAPI, Python
* **Machine Learning:** Scikit-Learn (`IsolationForest`), Pandas, NumPy
* **AI Integration:** Google Gemini API (Prompt Engineering for anomaly explanation)
* **Architecture:** RESTful API

## ⚙️ How It Works
1. **Data Ingestion:** Receives campaign data via POST request (`/analyze`).
2. **Anomaly Detection:** `IsolationForest` scans the dataset for anomalies (e.g., high cost with zero conversions).
3. **AI Evaluation:** Anomalous rows are sent to the Gemini API with a strict system prompt to evaluate the severity and reason for the anomaly.
4. **Response:** Returns a structured JSON containing raw data and the AI analyst's verdict.

## 🚀 Quick Start

1. Clone the repository:
   ```bash
   git clone [https://github.com/romaro23/traffic-anomaly-agent.git](https://github.com/romaro23/traffic-anomaly-agent.git)
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Set up your environment variables (create a .env file):
   ```bash
   GEMINI_API_KEY=your_api_key_here
4. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload
