import os
import torch
from sentinel_delta.core.model import SimpleAnomalyDetector, TorchModelWrapper


def main():
    model = SimpleAnomalyDetector(input_dim=4)
    # simple one-pass save — in real life run trainer
    path = os.environ.get("MODEL_PATH", "./models/seed_model.pt")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    wrapper = TorchModelWrapper(model, model_path=path)
    wrapper.save(path)
    print(f"Saved seed model to {path}")


if __name__ == "__main__":
    main()
