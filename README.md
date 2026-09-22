# Traffic Anomaly Agent 🚀

An AI-integrated backend microservice designed to automatically detect fraudulent traffic and budget anomalies in advertising campaigns. It now features **RAG (Retrieval-Augmented Generation)** memory to remember past anomalies and contextualize future analysis.

## 💼 Business Value
In performance marketing and traffic arbitrage, late reaction to bot traffic or overspending can drain budgets in hours. This service processes synthetic campaign metrics (clicks, leads, revenue, cost) and flags statistical outliers. It then leverages LLM to generate clear, business-readable alerts for media buyers, learning from historical occurrences to detect recurring patterns.

## 🛠️ Tech Stack
* **Backend:** FastAPI, Python
* **Machine Learning:** Scikit-Learn (`IsolationForest`), Pandas, NumPy
* **Vector Database (Memory):** ChromaDB 
* **AI Integration:** Google Gemini API (Prompt Engineering & RAG context building)
* **Architecture:** RESTful API

## ⚙️ How It Works
1. **Data Ingestion:** Receives campaign data via POST request (`/analyze`).
2. **Anomaly Detection:** `IsolationForest` scans the dataset for anomalies (e.g., high cost with zero conversions).
3. **Retrieval-Augmented Memory (RAG):** Checks ChromaDB for similar past anomalies (historical context) and attaches them to the new data. Every new anomaly is automatically saved back to the database.
4. **AI Evaluation:** Anomalous rows, along with historical context, are sent to the Gemini API with a strict system prompt to evaluate the severity and provide a verdict.
5. **Response:** Returns a structured JSON containing raw data and the AI analyst's verdict.

## 🔌 API Endpoints
- **POST `/analyze`**: Analyzes an array of campaign metrics for anomalies.
- **GET `/memory`**: Returns all historical anomaly records stored in ChromaDB.

## 🚀 Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/romaro23/traffic-anomaly-agent.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your environment variables (create a `.env` file):
   ```bash
   GEMINI_API_KEY=your_api_key_here
   ```
4. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```
5. **(New) Run the Test Script:** In a separate terminal, test the flow with randomly generated traffic data:
   ```bash
   python test.py
   ```
