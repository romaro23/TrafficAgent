from pydantic import BaseModel

class CampaignMetrics(BaseModel):
    campaign_id: str
    clicks: int
    cost: float
    leads: int
    revenue: float

class AnalyzeResponse(BaseModel):
    status: str
    analysis: str | None = None
    raw_anomalies: list[dict] | None = None
    message: str | None = None