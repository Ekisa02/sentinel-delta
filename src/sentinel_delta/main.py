from fastapi import FastAPI
from .api.routes import router
from .db.store import init_db
from .utils.logger import logger

app = FastAPI(title="Sentinel Delta - DeFi Smart Contract Analytics")
app.include_router(router, prefix="/api")

@app.on_event("startup")
def on_startup():
    logger.info("Starting Sentinel Delta")
    init_db()

@app.get("/")
def root():
    return {"service": "sentinel_delta", "status": "running"}
