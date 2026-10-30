import torch
import numpy as np
from .model import SimpleAnomalyDetector, TorchModelWrapper
from .processor import events_to_features, df_to_numpy
from ..config import settings


class Predictor:
    def __init__(self, model_path: str = None):
        self.model_path = model_path or settings.DEFAULT_MODEL_PATH
        # placeholder dimension; in real system should be inferred.
        self.input_dim = 4
        self.net = SimpleAnomalyDetector(self.input_dim)
        self.wrapper = TorchModelWrapper(self.net, model_path=self.model_path)
        try:
            if self.model_path and os.path.exists(self.model_path):
                self.wrapper.load(self.model_path)
        except Exception:
            # ignore missing model for initial dev
            pass

    def predict_from_events(self, events: list):
        df = events_to_features(events)
        arr = df_to_numpy(df)
        if len(arr) == 0:
            return []
        x = torch.from_numpy(arr)
        errs = self.wrapper.predict(x)
        return errs.numpy().tolist()
