from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi import Depends
from typing import Any
from ..api.schemas import PredictRequest, PredictResponse, TrainRequest
from ..core.ingest import fetch_contract_history
from ..core.predictor import Predictor
from ..db.store import upsert_contract, get_contract
from ..services.background import async_train_job
from ..utils.logger import logger

router = APIRouter()
predictor = Predictor()


@router.get("/health")
def health() -> Any:
    return {"status": "ok"}


@router.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    events = [e.dict() for e in req.events]
    logger.info("Received predict request for %d events", len(events))
    anomalies = predictor.predict_from_events(events)
    return PredictResponse(anomalies=anomalies, meta={"count": len(anomalies)})


@router.post("/train")
def train(req: TrainRequest, background_tasks: BackgroundTasks):
    # delegate to background job to keep endpoint responsive
    background_tasks.add_task(async_train_job, req.epochs, req.lr)
    return {"status": "started", "epochs": req.epochs}


@router.get("/contracts/{address}")
def get_contract_stats(address: str):
    record = get_contract(address)
    if not record:
        raise HTTPException(status_code=404, detail="contract not found")
    return record


@router.post("/ingest/{address}")
async def ingest_contract(address: str):
    # fetch some historical events and compute a basic aggregate metadata
    events = await fetch_contract_history(address, limit=50)
    anomalies = predictor.predict_from_events(events)
    meta = {"events": len(events), "anomaly_stats": {"max": max(anomalies) if anomalies else None, "mean": float(sum(anomalies) / len(anomalies)) if anomalies else None}}
    upsert_contract(address, meta)
    return {"address": address, "meta": meta}
