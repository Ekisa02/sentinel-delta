import os
import torch
import torch.nn as nn


class SimpleAnomalyDetector(nn.Module):
    """A simple MLP autoencoder-like structure for small tabular/time-window features."""

    def __init__(self, input_dim: int, hidden_dim: int = 32):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
        )
        self.decoder = nn.Sequential(
            nn.Linear(hidden_dim // 2, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, input_dim),
        )

    def forward(self, x):
        z = self.encoder(x)
        out = self.decoder(z)
        return out


class TorchModelWrapper:
    def __init__(self, model: nn.Module, model_path: str = None, device: str = None):
        self.model = model
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.model_path = model_path

    def predict(self, x: torch.Tensor) -> torch.Tensor:
        self.model.eval()
        x = x.to(self.device)
        with torch.no_grad():
            recon = self.model(x)
        # simple reconstruction error
        err = torch.mean((x - recon) ** 2, dim=1)
        return err.cpu()

    def save(self, path: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        torch.save(self.model.state_dict(), path)

    def load(self, path: str):
        self.model.load_state_dict(torch.load(path, map_location=self.device))
