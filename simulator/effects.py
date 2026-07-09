"""
effects.py

Process effects used by the semiconductor yield simulator.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np

from simulator.recipe import Recipe
from simulator.equipment import Equipment


# =====================================================
# Base Effect
# =====================================================

class ProcessEffect(ABC):
    """
    Abstract base class for all process effects.
    """

    @abstractmethod
    def evaluate(
        self,
        recipe: Recipe,
        equipment: Equipment,
    ) -> float:
        pass


# =====================================================
# Utility
# =====================================================

def gaussian(
    x: float,
    optimum: float,
    sigma: float,
) -> float:

    return float(
        np.exp(
            -((x - optimum) ** 2)
            / (2 * sigma ** 2)
        )
    )


# =====================================================
# Individual Effects
# =====================================================

class TemperatureEffect(ProcessEffect):

    def evaluate(
        self,
        recipe: Recipe,
        equipment: Equipment,
    ) -> float:

        return 0.08 * gaussian(
            recipe.temperature,
            optimum=660,
            sigma=10,
        )


class PressureEffect(ProcessEffect):

    def evaluate(
        self,
        recipe: Recipe,
        equipment: Equipment,
    ) -> float:

        return 0.06 * gaussian(
            recipe.pressure,
            optimum=20,
            sigma=2.5,
        )


class RFPowerEffect(ProcessEffect):

    def evaluate(
        self,
        recipe: Recipe,
        equipment: Equipment,
    ) -> float:

        return 0.05 * gaussian(
            recipe.rf_power,
            optimum=100,
            sigma=12,
        )


class GasFlowEffect(ProcessEffect):

    def evaluate(
        self,
        recipe: Recipe,
        equipment: Equipment,
    ) -> float:

        return 0.04 * gaussian(
            recipe.gas_flow,
            optimum=50,
            sigma=6,
        )


# =====================================================
# Interaction Effects
# =====================================================

class TemperaturePressureInteraction(ProcessEffect):

    def evaluate(
        self,
        recipe: Recipe,
        equipment: Equipment,
    ) -> float:

        return (
            0.02
            * gaussian(recipe.temperature, 660, 10)
            * gaussian(recipe.pressure, 20, 3)
        )


class RFGasInteraction(ProcessEffect):

    def evaluate(
        self,
        recipe: Recipe,
        equipment: Equipment,
    ) -> float:

        return (
            0.015
            * gaussian(recipe.rf_power, 100, 12)
            * gaussian(recipe.gas_flow, 50, 6)
        )


# =====================================================
# Equipment Effect
# =====================================================

class EquipmentEffect(ProcessEffect):

    def evaluate(
        self,
        recipe: Recipe,
        equipment: Equipment,
    ) -> float:

        return (
            equipment.efficiency - 1.0
        )


# =====================================================
# Future Extensions
# =====================================================

class RandomNoiseEffect(ProcessEffect):
    """
    Placeholder for future stochastic effects.

    Noise will be handled separately
    inside YieldModel.
    """

    def evaluate(
        self,
        recipe: Recipe,
        equipment: Equipment,
    ) -> float:

        return 0.0
