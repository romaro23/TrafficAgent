import json
import requests

from app.ml.core_ml import generate_traffic_data

print("Generating test traffic...")
df = generate_traffic_data(n_samples=50)
payload = df.to_dict(orient="records")

print(f"Sending {len(payload)} records for analysis...\n")
print("-" * 50)

try:
    response = requests.post("http://127.0.0.1:8000/api/analyze", json=payload)
    response.raise_for_status()

    result = response.json()

    print(f"STATUS: {result.get('status', 'unknown').upper()}\n")

    if result.get("status") == "anomalies_detected":
        print("ANALYSIS VERDICT:")
        print(result.get("analysis"))
        print("\n" + "-" * 50)

        print("RAW ANOMALIES DATA:")
        print(json.dumps(result.get("raw_anomalies"), indent=4))

    else:
        print(f"MESSAGE: {result.get('message')}")

except requests.exceptions.ConnectionError:
    print("Error: Failed to connect to the server.")
    print("Ensure the server is running (e.g. uvicorn app.main:app --reload).")
except Exception as e:
    print(f"Error: {e}")
