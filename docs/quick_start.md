# Quick start

1. Create virtual env and install dependencies
2. Run uvicorn sentinel_delta.main:app --reload
3. POST to /api/predict with simple events (see example_requests.http)
4. Use scripts/train_sample_model.py to generate a saved model
