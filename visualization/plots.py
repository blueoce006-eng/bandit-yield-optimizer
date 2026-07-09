"""
plots.py

Visualization utilities for benchmark results.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


class Plotter:
    """
    Plot benchmark results.
    """

    def __init__(self, save_dir="results/figures"):

        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    # -------------------------------------------------

    def reward_curve(self, results):

        plt.figure(figsize=(10, 5))

        for result in results:

            plt.plot(
                result.cumulative_reward,
                label=result.name,
            )

        plt.xlabel("Episode")
        plt.ylabel("Cumulative Reward")
        plt.title("Cumulative Reward")
        plt.grid(True)
        plt.legend()

        plt.tight_layout()

        plt.savefig(
            self.save_dir / "reward_curve.png",
            dpi=200,
        )

        plt.close()

    # -------------------------------------------------

    def yield_curve(self, results):

        plt.figure(figsize=(10, 5))

        for result in results:

            running_mean = np.cumsum(
                result.yields
            ) / np.arange(
                1,
                len(result.yields) + 1,
            )

            plt.plot(
                running_mean,
                label=result.name,
            )

        plt.xlabel("Episode")
        plt.ylabel("Average Yield")

        plt.title("Average Yield")

        plt.grid(True)

        plt.legend()

        plt.tight_layout()

        plt.savefig(
            self.save_dir / "yield_curve.png",
            dpi=200,
        )

        plt.close()

    # -------------------------------------------------

    def profit_curve(self, results):

        plt.figure(figsize=(10, 5))

        for result in results:

            running_profit = np.cumsum(
                result.profits
            )

            plt.plot(
                running_profit,
                label=result.name,
            )

        plt.xlabel("Episode")

        plt.ylabel("Cumulative Profit")

        plt.title("Profit Comparison")

        plt.grid(True)

        plt.legend()

        plt.tight_layout()

        plt.savefig(
            self.save_dir / "profit_curve.png",
            dpi=200,
        )

        plt.close()

    # -------------------------------------------------

    def arm_histogram(self, results):

        plt.figure(figsize=(10, 5))

        for result in results:

            plt.hist(
                result.selected_arms,
                bins=30,
                alpha=0.4,
                label=result.name,
            )

        plt.xlabel("Recipe ID")

        plt.ylabel("Selections")

        plt.title("Arm Selection Distribution")

        plt.legend()

        plt.tight_layout()

        plt.savefig(
            self.save_dir / "arm_histogram.png",
            dpi=200,
        )

        plt.close()

    # -------------------------------------------------

    def summary(self, results):

        self.reward_curve(results)

        self.yield_curve(results)

        self.profit_curve(results)

        self.arm_histogram(results)

        print()

        print("=" * 60)

        print("Figures saved to")

        print(self.save_dir)

        print("=" * 60)
