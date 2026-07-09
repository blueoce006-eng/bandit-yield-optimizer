"""
Gaussian Thompson Sampling.
"""

from __future__ import annotations

import numpy as np

from algorithms.base import BanditAlgorithm


class ThompsonSampling(BanditAlgorithm):

    def __init__(

        self,

        n_arms,

        prior_mean=0.0,

        prior_variance=1.0,

        observation_variance=1.0,

        rng=None,

    ):

        super().__init__(

            n_arms=n_arms,

            rng=rng,

        )

        self.prior_mean = prior_mean

        self.prior_variance = prior_variance

        self.observation_variance = observation_variance

        self.posterior_mean = np.full(

            n_arms,

            prior_mean,

        )

        self.posterior_variance = np.full(

            n_arms,

            prior_variance,

        )

    # ---------------------------------------------

    def select_arm(self):

        samples = self.rng.normal(

            self.posterior_mean,

            np.sqrt(

                self.posterior_variance

            ),

        )

        return int(

            np.argmax(

                samples

            )

        )

    # ---------------------------------------------

    def update(

        self,

        arm,

        reward,

    ):

        prior_mean = self.posterior_mean[arm]

        prior_var = self.posterior_variance[arm]

        obs_var = self.observation_variance

        posterior_var = (

            1

            /

            (

                1/prior_var

                +

                1/obs_var

            )

        )

        posterior_mean = (

            posterior_var

            *

            (

                prior_mean/prior_var

                +

                reward/obs_var

            )

        )

        self.posterior_mean[arm] = posterior_mean

        self.posterior_variance[arm] = posterior_var

        super().update(

            arm,

            reward,

        )
