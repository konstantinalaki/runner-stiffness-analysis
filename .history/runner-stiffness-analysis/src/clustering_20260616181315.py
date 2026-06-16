import pandas as pd
from pathlib import Path

from ruamel import yaml

ROOT_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT_DIR / "config.yaml"

with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

def remap(value, from_min, from_max, to_min, to_max):
    if from_max == from_min:
        return pd.Series(to_min, index=value.index)  # or to_max, or 0.5
    normalized = (value - from_min) / (from_max - from_min)
    return to_min + normalized * (to_max - to_min)

def load_data(file_path):
    return pd.read_csv(file_path)

def cluster_runners_gh(df):
    labels = config["clustering"]["labels"]
    q = config["clustering"]["q"]

    weight_min = df["runner_weight_kg"].min()
    weight_max = df["runner_weight_kg"].max()
    force_min = df["impact_force_newtons"].min()
    force_max = df["impact_force_newtons"].max()

    norm_weight = remap(df["runner_weight_kg"], weight_min, weight_max, 0.0, 1.0)
    norm_force = remap(df["impact_force_newtons"], force_min, force_max, 0.0, 1.0)
    
    df["load_score"] = round(0.5 * norm_weight + 0.5 * norm_force
    df["stiffness_profile"] = pd.qcut(df["load_score"], q=q, labels=labels)

    return df

def main():
    cleaned_data_path = ROOT_DIR / 'data' / 'processed' / 'runners_cleaned.csv'
    clustered_data_path = ROOT_DIR / 'data' / 'clustered' / 'runners_clustered.csv'
    
    # Load data
    df = load_data(cleaned_data_path)

    # Cluster runners
    df = cluster_runners_gh(df)
    
    # Save cleaned and clustered data
    df.to_csv(clustered_data_path, index=False)

if __name__ == "__main__":
    main()