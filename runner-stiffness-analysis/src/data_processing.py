import pandas as pd
from pathlib import Path

from ruamel import yaml

ROOT_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT_DIR / "config.yaml"

with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

def load_data(file_path):
    """Load the runner data from a CSV file."""
    data = pd.read_csv(file_path)
    return data

def clean_data(data):
    """Clean the dataset by handling missing values and standardizing formats."""
    # Drop rows with missing values
    data = data.dropna()
    
    # Convert numeric columns to numbers; invalid values become NaN
    numeric_cols = ["runner_weight_kg", "impact_force_newtons", "preferred_shoe_size"]
    for col in numeric_cols:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors="coerce")

    # Drop rows with missing values in any column
    data = data.dropna()

    return data

def remove_outliers(
    data,
    weight_min=None,
    weight_max=None,
    force_min=None,
    force_max=None,
    shoe_min=None,
    shoe_max=None,
):
    
    """Load from config file if not provided."""
    thresholds = config["data_processing"]
    weight_min = weight_min if weight_min is not None else thresholds["weight_min"]
    weight_max = weight_max if weight_max is not None else thresholds["weight_max"]
    force_min = force_min if force_min is not None else thresholds["force_min"]
    force_max = force_max if force_max is not None else thresholds["force_max"]
    shoe_min = shoe_min if shoe_min is not None else thresholds["shoe_min"]
    shoe_max = shoe_max if shoe_max is not None else thresholds["shoe_max"]
    
    """Remove rows outside realistic runner measurement ranges."""
    df = data.copy()

    if "runner_weight_kg" in df.columns:
        df = df[(df["runner_weight_kg"] >= weight_min) & (df["runner_weight_kg"] <= weight_max)]

    if "impact_force_newtons" in df.columns:
        df = df[(df["impact_force_newtons"] >= force_min) & (df["impact_force_newtons"] <= force_max)]

    if "preferred_shoe_size" in df.columns:
        df = df[(df["preferred_shoe_size"] >= shoe_min) & (df["preferred_shoe_size"] <= shoe_max)]
        
    return df


def save_cleaned_data(data, output_path):
    """Save the cleaned dataset to a CSV file."""
    data.to_csv(output_path, index=False)

def main():
    raw_data_path = ROOT_DIR / 'data' / 'raw' / 'runners.csv'
    cleaned_data_path = ROOT_DIR / 'data' / 'processed' / 'runners_cleaned.csv'
    
    # Load the data
    runner_data = load_data(raw_data_path)
    
    # Clean the data
    runner_data_cleaned = clean_data(runner_data)
    
    # Remove outliers
    runner_data_cleaned = remove_outliers(runner_data_cleaned)
    
    # Save the cleaned data
    save_cleaned_data(runner_data_cleaned, cleaned_data_path)

if __name__ == "__main__":
    main()