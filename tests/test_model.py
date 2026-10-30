import torch
from sentinel_delta.core.model import SimpleAnomalyDetector, TorchModelWrapper


def test_model_forward_and_save(tmp_path):
    model = SimpleAnomalyDetector(input_dim=4)
    x = torch.randn(8, 4)
    out = model(x)
    assert out.shape == x.shape

    path = tmp_path / "m.pt"
    wrapper = TorchModelWrapper(model, model_path=str(path))
    wrapper.save(str(path))
    assert path.exists()

    # load back
    new_model = SimpleAnomalyDetector(input_dim=4)
    new_wrapper = TorchModelWrapper(new_model, model_path=str(path))
    new_wrapper.load(str(path))


def test_predictor_error_nonnegative():
    # prediction should return non-negative reconstruction errors
    from sentinel_delta.core.predictor import Predictor

    p = Predictor()
    events = [{"contract": "0x0", "nonce": 1, "value": 1.0, "gas_used": 21000, "timestamp": 1}]
    errs = p.predict_from_events(events)
    assert all(e >= 0 for e in errs)
