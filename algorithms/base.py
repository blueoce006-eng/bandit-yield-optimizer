"""
base.py

Abstract base class for Multi-Armed Bandit algorithms.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
import numpy as np


class BanditAlgorithm(ABC):
    """
    Base class for all bandit algorithms.
    """

    def __init__(
        self,
        n_arms: int,
        rng: np.random.Generator | None = None,
    ):

        self.n_arms = n_arms

        self.rng = (
            rng
            if rng is not None
            else np.random.default_rng()
        )

        self.reset()

    # -------------------------------------------------

    def reset(self):
        """
        Reset algorithm state.
        """

        self.t = 0

        self.counts = np.zeros(
            self.n_arms,
            dtype=np.int64,
        )

        self.values = np.zeros(
            self.n_arms,
            dtype=float,
        )

        self.total_reward = 0.0

    # -------------------------------------------------

    @abstractmethod
    def select_arm(self) -> int:
        """
        Return the index of the selected arm.
        """
        raise NotImplementedError

    # -------------------------------------------------

    def update(
        self,
        arm: int,
        reward: float,
    ):

        self.t += 1

        self.counts[arm] += 1

        n = self.counts[arm]

        value = self.values[arm]

        self.values[arm] = value + (
            reward - value
        ) / n

        self.total_reward += reward

    # -------------------------------------------------

    @property
    def average_reward(self):

        if self.t == 0:
            return 0.0

        return self.total_reward / self.t

    # -------------------------------------------------

    @property
    def best_arm(self):

        return int(
            np.argmax(self.values)
        )

    # -------------------------------------------------

    def statistics(self):

        return {

            "steps": self.t,

            "average_reward": self.average_reward,

            "best_arm": self.best_arm,

            "counts": self.counts.copy(),

            "values": self.values.copy(),

        }

    # -------------------------------------------------

    def __repr__(self):

        return (

            f"{self.__class__.__name__}("

            f"steps={self.t}, "

            f"best_arm={self.best_arm})"

        )
