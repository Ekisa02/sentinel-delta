import asyncio
import os
import torch
from ..core.model import SimpleAnomalyDetector, TorchModelWrapper
from ..utils.logger import logger
from ..config import settings


async def train_loop(model: SimpleAnomalyDetector, epochs: int = 5, lr: float = 1e-3):
    # Dummy train loop with random data for demonstration. Replace with real dataset.
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    for epoch in range(epochs):
        x = torch.randn(64, 4)
        recon = model(x)
        loss = torch.nn.functional.mse_loss(recon, x)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        logger.info("Epoch %d loss=%.4f", epoch + 1, loss.item())
        await asyncio.sleep(0)  # yield to event loop


def sync_train_job(epochs: int = 5, lr: float = 1e-3):
    model = SimpleAnomalyDetector(input_dim=4)
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(train_loop(model, epochs=epochs, lr=lr))
        path = settings.DEFAULT_MODEL_PATH
        os.makedirs(os.path.dirname(path), exist_ok=True)
        wrapper = TorchModelWrapper(model, model_path=path)
        wrapper.save(path)
        logger.info("Saved model to %s", path)
    finally:
        loop.close()


def async_train_job(epochs: int = 5, lr: float = 1e-3):
    # wrapper to be scheduled from FastAPI (background task) — runs in threadpool
    logger.info("Starting async_train_job epochs=%d lr=%s", epochs, lr)
    sync_train_job(epochs, lr)
