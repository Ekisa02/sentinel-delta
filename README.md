# Sentinel Delta

Sentinel Delta is a modular DeFi Smart Contract Analytics platform built with FastAPI and PyTorch. It provides data ingestion hooks, a simple feature processing pipeline, a trainable PyTorch anomaly-detection model, REST endpoints for inference and model operations, background job integration, and lightweight storage for analytic state.

Key features
- FastAPI-powered API for serving inference and model lifecycle endpoints
- PyTorch-based models and training utilities (example training script included)
- Pluggable ingestion module (on-chain RPC/webhooks placeholder) for streaming events
- Data processing and feature creation utilities tailored for DeFi event streams
- Background tasks and job integration
- Tests, docs, and developer tooling

Architecture overview

- src/sentinel_delta/main.py: API entry point (FastAPI)
- src/sentinel_delta/api: API route definitions and request/response schemas
- src/sentinel_delta/core: Core components (ingestion, processing, model wrapping, predictor)
- src/sentinel_delta/services: Background job(s), scheduler stubs
- src/sentinel_delta/db: Lightweight persistence layer (SQLite via SQLAlchemy)
- scripts/: Example training and model export scripts
- tests/: Unit and integration tests
- docs/: Architecture and usage notes

Installation

Prerequisites:
- Python 3.9+ (3.10 recommended)
- Git
- (Optional) CUDA-enabled PyTorch for GPU

Clone and install

```bash
git clone https://github.com/your-org/sentinel-delta.git
cd sentinel-delta
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run locally

```bash
uvicorn sentinel_delta.main:app --reload --host 0.0.0.0 --port 8000
```

API

- GET /health -> service health
- POST /predict -> run inference given a minimal event payload
- POST /train -> trigger a simple training operation (example endpoint)
- GET /contracts/{address} -> retrieve stored contract analytics

See docs/usage.md for example requests and developer notes.

Development notes

- Use the included scripts/train_sample_model.py to create a sample model and save it into the (configurable) model path.
- Tests use pytest; run `pytest -q`.

Contributing

PRs welcome. Please follow the usual GitHub workflow and include tests for new features.

License

MIT (see LICENSE file)
