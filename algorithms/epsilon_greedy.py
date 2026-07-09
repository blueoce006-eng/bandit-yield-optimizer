"""
epsilon_greedy.py

Epsilon-Greedy Bandit with epsilon decay.
"""

from __future__ import annotations

from algorithms.base import BanditAlgorithm


class EpsilonGreedy(BanditAlgorithm):
    """
    Epsilon-Greedy algorithm with exponential decay.

    Parameters
    ----------
    n_arms : int
        Number of arms.

    epsilon : float
        Initial exploration probability.

    decay : float
        Multiplicative decay factor.

    minimum : float
        Minimum exploration probability.
    """

    def __init__(
        self,
        n_arms: int,
        epsilon: float = 0.30,
        decay: float = 0.995,
        minimum: float = 0.01,
        rng=None,
    ):

        self.initial_epsilon = epsilon
        self.epsilon = epsilon
        self.decay = decay
        self.minimum = minimum

        super().__init__(
            n_arms=n_arms,
            rng=rng,
        )

    # -------------------------------------------------

    def select_arm(self) -> int:
        """
        Choose an arm using epsilon-greedy.
        """

        # Exploration
        if self.rng.random() < self.epsilon:

            return int(
                self.rng.integers(
                    self.n_arms
                )
            )

        # Exploitation
        return self.best_arm

    # -------------------------------------------------

    def update(
        self,
        arm: int,
        reward: float,
    ):

        super().update(
            arm,
            reward,
        )

        self.epsilon = max(
            self.minimum,
            self.epsilon * self.decay,
        )

    # -------------------------------------------------

    def reset(self):

        super().reset()

        self.epsilon = self.initial_epsilon

    # -------------------------------------------------

    def statistics(self):

        stats = super().statistics()

        stats["epsilon"] = self.epsilon

        return stats
