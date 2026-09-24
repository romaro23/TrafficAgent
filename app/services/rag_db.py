import chromadb
import uuid

class AnomaliesMemory:
    def __init__(self, db_path: str = "./chroma_data"):
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection("anomalies")

    def remember_anomaly(self, campaign_id: str, description: str, metrics: dict):
        record_id = f"{campaign_id}_{uuid.uuid4().hex[:8]}"

        self.collection.add(
            documents=[description],
            metadatas=[metrics],
            ids=[record_id]
        )

    def recall_similar(self, query_description: str, n_results: int = 2) -> list:
        if self.collection.count() == 0:
            return []

        results = self.collection.query(
            query_texts=[query_description],
            n_results=n_results
        )

        if results['documents'] and results['documents'][0]:
            return results['documents'][0]

        return []

    def get_all_memory(self):
        if self.collection.count() == 0:
            return {"message": "The base is empty"}

        return self.collection.get()