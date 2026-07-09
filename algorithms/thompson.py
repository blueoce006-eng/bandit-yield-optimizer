"""
thompson.py

Gaussian Thompson Sampling for continuous rewards.
"""

from __future__ import annotations

import numpy as np

from algorithms.base import BanditAlgorithm


class ThompsonSampling(BanditAlgorithm):
    """
    Gaussian Thompson Sampling.

    Assumptions
    -----------
    - Continuous rewards
    - Gaussian likelihood
    - Independent arms
    """

    def __init__(
        self,
        n_arms: int,
        prior_mean: float = 0.0,
        prior_precision: float = 1.0,
        reward_precision: float = 1.0,
        rng=None,
    ):

        super().__init__(
            n_arms=n_arms,
            rng=rng,
        )

        self.prior_mean = prior_mean
        self.prior_precision = prior_precision
        self.reward_precision = reward_precision

        self.posterior_mean = np.full(
            n_arms,
            prior_mean,
            dtype=float,
        )

        self.posterior_precision = np.full(
            n_arms,
            prior_precision,
            dtype=float,
        )

    # -------------------------------------------------

    def select_arm(self) -> int:
        """
        Sample one value from each posterior.
        """

        variance = 1.0 / self.posterior_precision

        samples = self.rng.normal(
            self.posterior_mean,
            np.sqrt(variance),
        )

        return int(np.argmax(samples))

    # -------------------------------------------------

    def update(
        self,
        arm: int,
        reward: float,
    ):

        precision = (
            self.posterior_precision[arm]
            + self.reward_precision
        )

        mean = (
            self.posterior_precision[arm]
            * self.posterior_mean[arm]
            + self.reward_precision
            * reward
        ) / precision

        self.posterior_precision[arm] = precision
        self.posterior_mean[arm] = mean

        super().update(
            arm,
            reward,
        )

    # -------------------------------------------------

    def reset(self):

        super().reset()

        self.posterior_mean = np.full(
            self.n_arms,
            self.prior_mean,
            dtype=float,
        )

        self.posterior_precision = np.full(
            self.n_arms,
            self.prior_precision,
            dtype=float,
        )

    # -------------------------------------------------

    def statistics(self):

        stats = super().statistics()

        stats["posterior_mean"] = self.posterior_mean.copy()

        stats["posterior_variance"] = (
            1.0 / self.posterior_precision
        )

        return stats
