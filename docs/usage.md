# Usage

Start the service:

```bash
uvicorn sentinel_delta.main:app --reload
```

Health check

GET /api/health

Predict

POST /api/predict

Body: {"events": [{...}, ...]}

Returns: reconstruction error per event (a simple anomaly score).

Train

POST /api/train to schedule a sample training job. In production this endpoint should be access-controlled; the demo implementation spawns a local task which saves a model file.

Ingest

POST /api/ingest/{contract_address} simulates fetching historical events and computes a small meta summary with anomaly statistics.

Extending

- Replace ingest.fetch_contract_history with a real RPC, webhook or archive node connector.
- Replace the sample training loop with a dataset-backed training pipeline, metrics, and checkpoints.
- Add authentication and rate-limiting to API endpoints in front of production deployments.
