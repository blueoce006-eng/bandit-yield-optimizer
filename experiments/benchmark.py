"""
benchmark.py

Compare multiple bandit algorithms
on the semiconductor simulator.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from simulator.factory import Factory

from algorithms.random_policy import RandomPolicy
from algorithms.epsilon_greedy import EpsilonGreedy
from algorithms.ucb import UCB
from algorithms.thompson import ThompsonSampling


# ==========================================================
# Result
# ==========================================================

@dataclass(slots=True)
class BenchmarkResult:

    name: str

    rewards: list[float]

    profits: list[float]

    yields: list[float]

    cumulative_reward: list[float]

    selected_arms: list[int]


# ==========================================================
# Benchmark
# ==========================================================

class Benchmark:

    def __init__(

        self,

        episodes: int = 10000,

        seed: int = 42,

    ):

        self.episodes = episodes

        self.seed = seed

    # ------------------------------------------------------

    def run_algorithm(

        self,

        algorithm,

    ) -> BenchmarkResult:

        factory = Factory(

            seed=self.seed,

        )

        rewards = []

        profits = []

        yields = []

        cumulative_reward = []

        selected_arms = []

        cumulative = 0.0

        for _ in range(self.episodes):

            arm = algorithm.select_arm()

            result = factory.pull_arm(

                arm,

            )

            algorithm.update(

                arm,

                result.reward,

            )

            rewards.append(

                result.reward,

            )

            profits.append(

                result.profit,

            )

            yields.append(

                result.lot_yield,

            )

            cumulative += result.reward

            cumulative_reward.append(

                cumulative,

            )

            selected_arms.append(

                arm,

            )

        return BenchmarkResult(

            name=algorithm.__class__.__name__,

            rewards=rewards,

            profits=profits,

            yields=yields,

            cumulative_reward=cumulative_reward,

            selected_arms=selected_arms,

        )

    # ------------------------------------------------------

    def run(self):

        factory = Factory(

            seed=self.seed,

        )

        n_arms = factory.n_arms

        algorithms = [

            RandomPolicy(

                n_arms,

                rng=np.random.default_rng(self.seed),

            ),

            EpsilonGreedy(

                n_arms,

                rng=np.random.default_rng(self.seed),

            ),

            UCB(

                n_arms,

                rng=np.random.default_rng(self.seed),

            ),

            ThompsonSampling(

                n_arms,

                rng=np.random.default_rng(self.seed),

            ),

        ]

        results = []

        for algorithm in algorithms:

            print(

                f"Running {algorithm.__class__.__name__}..."

            )

            results.append(

                self.run_algorithm(

                    algorithm,

                )

            )

        return results


# ==========================================================
# Example
# ==========================================================

if __name__ == "__main__":

    benchmark = Benchmark(

        episodes=5000,

    )

    results = benchmark.run()

    for result in results:

        print()

        print(result.name)

        print(

            "Average Reward :",

            np.mean(result.rewards),

        )

        print(

            "Average Yield :",

            np.mean(result.yields),

        )

        print(

            "Average Profit :",

            np.mean(result.profits),

        )
