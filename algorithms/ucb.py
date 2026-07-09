"""
ucb.py

UCB1-Tuned algorithm.
"""

from __future__ import annotations

import numpy as np

from algorithms.base import BanditAlgorithm


class UCB(BanditAlgorithm):
    """
    UCB1-Tuned implementation.

    Reference:
    Auer et al., 2002
    """

    def __init__(

        self,

        n_arms,

        rng=None,

    ):

        super().__init__(

            n_arms=n_arms,

            rng=rng,

        )

        self.squared_rewards = np.zeros(
            n_arms,
            dtype=float,
        )

    # -------------------------------------------------

    def select_arm(self) -> int:

        # Play each arm once

        for arm in range(self.n_arms):

            if self.counts[arm] == 0:

                return arm

        total = self.t

        ucb_values = np.zeros(
            self.n_arms,
        )

        for arm in range(self.n_arms):

            mean = self.values[arm]

            n = self.counts[arm]

            variance = (

                self.squared_rewards[arm] / n

                - mean ** 2

            )

            variance = max(
                0.0,
                variance,
            )

            bonus = np.sqrt(

                (np.log(total) / n)

                * min(

                    0.25,

                    variance

                    + np.sqrt(

                        2 * np.log(total) / n

                    )

                )

            )

            ucb_values[arm] = (

                mean

                + bonus

            )

        return int(
            np.argmax(
                ucb_values
            )
        )

    # -------------------------------------------------

    def update(

        self,

        arm,

        reward,

    ):

        self.squared_rewards[arm] += (

            reward ** 2

        )

        super().update(

            arm,

            reward,

        )
