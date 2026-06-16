import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

def load_data(file_path):
    return pd.read_csv(file_path)

def plot_distribution_by_profile(df, output_dir):
    """Bar chart: number of runners per stiffness profile."""
    fig, ax = plt.subplots(figsize=(6, 4))
    df["stiffness_profile"].value_counts().plot(kind="bar", ax=ax, color=["#8ecae6", "#219ebc", "#023047"])
    ax.set_title("Runners per Stiffness Profile")
    ax.set_xlabel("Profile")
    ax.set_ylabel("Count")
    plt.tight_layout()
    plt.savefig(output_dir / "profile_distribution.png", dpi=150)
    plt.close()

def plot_clusters(df, output_dir):
    """Scatter plot: weight vs force, colored by profile."""
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.scatterplot(
        data=df,
        x="runner_weight_kg",
        y="impact_force_newtons",
        hue="stiffness_profile",
        palette={"Soft": "#8ecae6", "Medium": "#219ebc", "Firm": "#023047"},
        ax=ax
    )
    ax.set_title("Runner Clusters by Stiffness Profile")
    plt.tight_layout()
    plt.savefig(output_dir / "cluster_scatter.png", dpi=150)
    plt.close()

def main():
    clustered_data_path = ROOT_DIR / "data" / "clustered" / "runners_clustered.csv"
    output_dir = ROOT_DIR / "data" / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)

    df = load_data(clustered_data_path)

    plot_distribution_by_profile(df, output_dir)
    plot_clusters(df, output_dir)

if __name__ == "__main__":
    main()