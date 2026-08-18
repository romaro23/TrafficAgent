import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

def generate_traffic_data(n_samples: int = 1000, random_seed: int = 42) -> pd.DataFrame:
    np.random.seed(random_seed)

    campaign_ids = [f"CMP_{np.random.randint(100, 110)}" for _ in range(n_samples)]

    clicks = np.random.poisson(lam=300, size=n_samples)

    cpc = np.random.uniform(0.5, 1.2, size=n_samples)
    cost = clicks * cpc

    conversion_rate = np.random.uniform(0.02, 0.05, size=n_samples)
    leads = np.random.binomial(clicks, conversion_rate)

    payout_per_lead = 25.0
    revenue = leads * payout_per_lead

    df = pd.DataFrame({
        "campaign_id": campaign_ids,
        "clicks": clicks,
        "cost": np.round(cost, 2),
        "leads": leads,
        "revenue": np.round(revenue, 2)
    })

    n_anomalies = int(n_samples * 0.03)
    anomaly_indices = np.random.choice(n_samples, size=n_anomalies, replace=False)

    for idx in anomaly_indices:
        anomaly_type = np.random.choice(["bot_traffic", "cost_spike", "broken_tracker"])
        if anomaly_type == "bot_traffic":
            df.loc[idx, "clicks"] = df.loc[idx, "clicks"] * 3
            df.loc[idx, "leads"] = 0
            df.loc[idx, "revenue"] = 0.0
        elif anomaly_type == "cost_spike":
            df.loc[idx, "cost"] = df.loc[idx, "cost"] * 5
        elif anomaly_type == "broken_tracker":
            df.loc[idx, "revenue"] = 0.0

    return df

def detect_anomalies(data: pd.DataFrame) -> pd.DataFrame:
    data["CR"] = np.where(data["clicks"] > 0, (data["leads"] / data["clicks"] * 100), 0)
    data["CPL"] = np.where(data["leads"] > 0, (data["cost"] / data["leads"]), 0)
    data["ROI"] = np.where(data["cost"] > 0, ((data["revenue"] - data["cost"]) / data["cost"]) * 100, 0)

    data_to_model = data.drop(columns=["campaign_id"])

    model = IsolationForest(contamination=0.05, random_state=42)
    data["anomaly"] = model.fit_predict(data_to_model)

    anomalies = data[data["anomaly"] == -1]

    return anomalies

if __name__ == "__main__":
    data_test = generate_traffic_data()

    anomalies_test = detect_anomalies(data_test)

    print(f"Anomalies found: {len(anomalies_test)}")
    print(anomalies_test[["campaign_id", "clicks", "leads", "revenue", "cost", "CR", "ROI"]].head(10))