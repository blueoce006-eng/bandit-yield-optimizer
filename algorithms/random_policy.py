"""
random_policy.py

Random arm selection policy.
"""

from __future__ import annotations

from algorithms.base import BanditAlgorithm


class RandomPolicy(BanditAlgorithm):
    """
    Baseline algorithm.

    Selects an arm uniformly at random.
    """

    def select_arm(self) -> int:

        return int(
            self.rng.integers(
                low=0,
                high=self.n_arms,
            )
        )
