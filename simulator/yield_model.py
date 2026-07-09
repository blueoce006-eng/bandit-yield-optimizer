import numpy as np

from simulator.recipe import Recipe
from simulator.equipment import Equipment


class YieldModel:
    """
    Virtual semiconductor process model.
    """

    def __init__(self, noise_std: float = 0.005):

        self.noise_std = noise_std

    @staticmethod
    def gaussian(x, optimum, sigma):
        return np.exp(-((x - optimum) ** 2) / (2 * sigma ** 2))

    def expected_yield(
        self,
        recipe: Recipe,
        equipment: Equipment
    ) -> float:

        base = 0.70

        # ---------- Individual Process Effects ----------

        temp = 0.08 * self.gaussian(
            recipe.temperature,
            optimum=660,
            sigma=12,
        )

        pressure = 0.06 * self.gaussian(
            recipe.pressure,
            optimum=20,
            sigma=3,
        )

        rf = 0.05 * self.gaussian(
            recipe.rf_power,
            optimum=100,
            sigma=15,
        )

        gas = 0.04 * self.gaussian(
            recipe.gas_flow,
            optimum=50,
            sigma=8,
        )

        # ---------- Interaction ----------

        interaction1 = (
            0.02
            * self.gaussian(recipe.temperature, 660, 15)
            * self.gaussian(recipe.pressure, 20, 3)
        )

        interaction2 = (
            0.015
            * self.gaussian(recipe.rf_power, 100, 20)
            * self.gaussian(recipe.gas_flow, 50, 10)
        )

        # ---------- Equipment ----------

        equipment_effect = (
            equipment.health
            - equipment.contamination
        )

        expected = (
            base
            + temp
            + pressure
            + rf
            + gas
            + interaction1
            + interaction2
        )

        expected *= equipment_effect

        return float(np.clip(expected, 0.0, 1.0))

    def sample(
        self,
        recipe: Recipe,
        equipment: Equipment,
    ) -> float:

        mean = self.expected_yield(
            recipe,
            equipment,
        )

        measured = np.random.normal(
            mean,
            self.noise_std,
        )

        return float(np.clip(measured, 0.0, 1.0))
