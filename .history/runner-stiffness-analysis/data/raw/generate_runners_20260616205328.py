#!/usr/bin/env python3
"""Generate a synthetic runners dataset and save to data/raw/ runners.csv.

Creates 5000 rows with columns:
- runner_weight_kg
- impact_force_newtons
- preferred_shoe_size

About 2% of rows are deliberately broken/outliers (unrealistic weights, missing
values, negative forces, or text "ERROR").
"""
from pathlib import Path
import random
import numpy as np
import pandas as pd


SEED = 42
N = 5000
BROKEN_PCT = 0.02


def generate_dataset(seed=SEED, n=N, broken_pct=BROKEN_PCT):
    rng = np.random.default_rng(seed)

    # Weight: normal around 70kg, std 15, clip to realistic adult range
    weights = rng.normal(70, 15, size=n)
    weights = np.clip(weights, 40, 140)

    # Impact force: base around 1500N with std 400, correlated with weight
    base_force = rng.normal(1500, 400, size=n)
    # Add correlation: heavier runners tend toward higher force
    force = base_force + 6.0 * (weights - 70) + rng.normal(0, 100, size=n)

    # Shoe size: EU 36-48, normal around 42
    shoe = rng.normal(42, 1.5, size=n)
    shoe = np.clip(shoe, 36, 48)

    df = pd.DataFrame(
        {
            "runner_weight_kg": np.round(weights, 2),
            "impact_force_newtons": np.round(force, 2),
            "preferred_shoe_size": np.round(shoe, 1),
        }
    )

    # Inject broken/outlier rows (~2%)
    n_broken = max(1, int(n * broken_pct))
    broken_idx = rng.choice(n, size=n_broken, replace=False)

    for i in broken_idx:
        kind = rng.choice(["unreal_weight", "missing", "neg_force", "text_force"]) 
        if kind == "unreal_weight":
            # choose low or high unrealistic weight
            df.at[i, "runner_weight_kg"] = rng.choice([10.0, 300.0])
        elif kind == "missing":
            # set one or two random fields to empty string
            cols = ["runner_weight_kg", "impact_force_newtons", "preferred_shoe_size"]
            k = rng.choice([1, 2])
            cols_to_blank = rng.choice(cols, size=k, replace=False)
            for c in cols_to_blank:
                df.at[i, c] = ""
        elif kind == "neg_force":
            df.at[i, "impact_force_newtons"] = -abs(float(rng.normal(100, 50)))
        elif kind == "text_force":
            df.at[i, "impact_force_newtons"] = "ERROR"

    # Shuffle rows so outliers are mixed in
    df = df.sample(frac=1, random_state=seed).reset_index(drop=True)

    return df


def main():
    # Project root is parent of this scripts folder
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    out_path = PROJECT_ROOT / "data" / "raw" / "generated_runners.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    df = generate_dataset()
    df.to_csv(out_path, index=False)
    print(f"Wrote {len(df)} rows to {out_path}")


if __name__ == "__main__":
    main()
