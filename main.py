import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from core_ml import detect_anomalies
from model_access import send_request_to_model
from config import Config

class CampaignMetrics(BaseModel):
    campaign_id: str
    clicks: int
    cost: float
    leads: int
    revenue: float

app = FastAPI()

@app.post("/analyze")
def analyze_anomalies(payload: list[CampaignMetrics]):
    df = pd.DataFrame([item.model_dump() for item in payload])
    anomalies = detect_anomalies(df)

    if not anomalies.empty:
        anomalies_to_model = anomalies.to_dict(orient="records")

        prompt = (
            "Ты — строгий senior traffic analyst. Твоя задача: проанализировать "
            "этот JSON с аномальными рекламными кампаниями. Коротко и по делу укажи, "
            "где идет слив бюджета или бот-трафик. Без приветствий и воды. "
            f"Данные: {anomalies_to_model}"
        )

        response = send_request_to_model(prompt, Config.API_KEY)

        return {
            "status": "anomalies_detected",
            "analysis": response,
            "raw_anomalies": anomalies_to_model
        }
    else:
        return {"status": "ok", "message": "No anomalies found"}
