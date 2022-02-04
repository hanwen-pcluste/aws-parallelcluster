import json
from pathlib import Path

import click
import matplotlib.pyplot as plt

ALL_METRICS = [
    "jobRunTime",
    "jobWaitingTime",
    "jobWarmupLeaderNodeTime",
    "jobWarmupFirstNodeTime",
    "jobWarmupLastNodeTime",
    "osuLatencyMean",
    "instancePreInstallUpTime",
    "instancePostInstallUpTime",
]

ALL_CONFIGURATIONS = ["baseline", "msad1k", "msad1k-enumerate"]
ALL_NODES = [10]


@click.command()
@click.option("--datadir", help="Directory containing the dataset.", required=True, type=click.Path())
@click.option("--outdir", help="Directory where to create plots.", required=True, type=click.Path())
@click.option(
    "--configurations", help="Comma separated list of configurations.", required=True, default=ALL_CONFIGURATIONS
)
@click.option("--nodes", help="Comma separated list of nodes.", required=True, type=str, default=ALL_NODES)
@click.option("--metrics", help="Comma separated list of metrics.", required=True, type=str, default=ALL_METRICS)
def generate_plots(datadir, outdir, configurations, nodes, metrics):
    # Load samples
    samples = {}
    for configuration in configurations:
        samples[configuration] = {}
        for n in nodes:
            samples_file = f"{datadir}/{configuration}/{n}nodes/samples.json"
            with open(samples_file) as f:
                samples[configuration][str(n)] = json.load(f)

    for metric in metrics:

        # Create Dataset
        data_baseline = [[float(v) for v in samples["baseline"][str(n)][f"{metric}Sample"].split(",")] for n in nodes]
        data_msad1k = [[float(v) for v in samples["msad1k"][str(n)][f"{metric}Sample"].split(",")] for n in nodes]
        data_msad1k_enumerate = [
            [float(v) for v in samples["msad1k-enumerate"][str(n)][f"{metric}Sample"].split(",")] for n in nodes
        ]

        # Figure
        fig, ax = plt.subplots(figsize=(10, 5), layout="constrained")

        # Titles
        ax.set_title(f"AWS ParallelCluster\n{metric}", fontweight="bold")
        ax.set_xlabel("Compute Nodes", fontweight="bold")
        ax.set_ylabel("Time (ms)", fontweight="bold")

        n_configurations = len(configurations)
        n_nodes = len(nodes)
        positions = [i for i in range(1, n_configurations * n_nodes + 1)]

        # Box Plots
        bp_baseline = ax.boxplot(
            data_baseline,
            patch_artist=True,
            boxprops=dict(facecolor="palegreen"),
            labels=nodes,
            positions=[i for i in positions if i % n_configurations == 1],
        )
        bp_msad1k = ax.boxplot(
            data_msad1k,
            patch_artist=True,
            boxprops=dict(facecolor="steelblue"),
            labels=nodes,
            positions=[i for i in positions if i % n_configurations == 2],
        )
        bp_msad1k_enumerate = ax.boxplot(
            data_msad1k_enumerate,
            patch_artist=True,
            boxprops=dict(facecolor="lightcoral"),
            labels=nodes,
            positions=[i for i in positions if i % n_configurations == 0],
        )

        # Ticks
        ax.set_xticklabels(
            [str(nodes[int(i / n_configurations) - 1]) if i % n_configurations == 0 else "" for i in positions]
        )

        # Legend
        ax.legend(
            [bp_baseline["boxes"][0], bp_msad1k["boxes"][0], bp_msad1k_enumerate["boxes"][0]],
            configurations,
            loc="upper left",
        )

        # Plot
        file = Path(f"{outdir}/{metric}.png")
        file.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(file.absolute())


if __name__ == "__main__":
    generate_plots()
