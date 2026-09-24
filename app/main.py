from fastapi import FastAPI
from app.api.routes import router as analyze_router

app = FastAPI(
    title="TrafficAgent API"
)

app.include_router(analyze_router, prefix="/api", tags=["Analysis"])

@app.get("/")
def health_check():
    return {"status": "healthy", "service": "TrafficAgent"}