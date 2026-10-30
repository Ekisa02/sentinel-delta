import numpy as np
import pandas as pd
from typing import List, Dict, Any


def events_to_features(events: List[Dict[str, Any]]) -> pd.DataFrame:
    """Convert a list of event dicts into a features DataFrame.

    This is a simple example feature engineering step suitable for time-series anomaly detection.
    """
    df = pd.DataFrame(events)
    # Basic derived features
    df = df.sort_values(by=["timestamp", "nonce"]).reset_index(drop=True)
    df["value_log"] = np.log1p(df.get("value", 0))
    df["gas_scaled"] = df.get("gas_used", 0) / 1e5
    df["delta_value"] = df["value"].diff().fillna(0)
    # Fill missing columns with zeros to make shape stable
    for col in ["value", "value_log", "gas_scaled", "delta_value"]:
        if col not in df:
            df[col] = 0
    return df[["value", "value_log", "gas_scaled", "delta_value"]]


def df_to_numpy(df: pd.DataFrame) -> np.ndarray:
    return df.values.astype(np.float32)
