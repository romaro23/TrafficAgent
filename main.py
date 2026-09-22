import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from core_ml import detect_anomalies
from model_access import send_request_to_model
from config import Config
from rag_db import AnomaliesMemory

class CampaignMetrics(BaseModel):
    campaign_id: str
    clicks: int
    cost: float
    leads: int
    revenue: float

app = FastAPI()
memory = AnomaliesMemory()

@app.get("/memory")
def view_memory():
    data = memory.get_all_memory()
    return data

@app.post("/analyze")
def analyze_anomalies(payload: list[CampaignMetrics]):
    df = pd.DataFrame([item.model_dump() for item in payload])
    anomalies = detect_anomalies(df)

    if not anomalies.empty:
        anomalies_to_model = anomalies.to_dict(orient="records")
        historical_context = ""

        for anomaly in anomalies_to_model:
            camp_id = anomaly["campaign_id"]
            anomaly_desc = f"Campaign {camp_id} metrics: clicks {anomaly['clicks']}, leads {anomaly['leads']}, cost {anomaly['cost']}, revenue {anomaly['revenue']}."

            similar_past_cases = memory.recall_similar(anomaly_desc)
            if similar_past_cases:
                historical_context += f"- Past similar cases for {camp_id}:\n  " + "\n  ".join(
                    similar_past_cases) + "\n"

            memory.remember_anomaly(
                campaign_id=camp_id,
                description=anomaly_desc,
                metrics=anomaly
            )

        prompt = (
            "You are a strict senior traffic analyst. Your task is to analyze "
            "this JSON containing anomalous ad campaigns. Briefly and to the point, "
            "indicate where budget drain or bot traffic is occurring. No greetings or fluff.\n\n"
            f"Current Anomalies Data:\n{anomalies_to_model}\n\n"
            f"Historical Context (similar past anomalies):\n{historical_context if historical_context else 'No past similar cases found.'}\n\n"
            "Use the Historical Context to determine if this is a recurring issue or a new spike. Provide your final verdict."
        )

        response = send_request_to_model(prompt, Config.API_KEY)

        return {
            "status": "anomalies_detected",
            "analysis": response,
            "raw_anomalies": anomalies_to_model
        }
    else:
        return {"status": "ok", "message": "No anomalies found"}
