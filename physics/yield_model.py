"""
yield_model.py

Semiconductor yield model.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np

from simulator.recipe import Recipe
from simulator.equipment import Equipment

from physics.effects import ProcessEffect


# =====================================================
# Result
# =====================================================

@dataclass(slots=True)
class YieldResult:

    expected: float

    measured: float


# =====================================================
# Yield Model
# =====================================================

class YieldModel:

    def __init__(
        self,
        effects: Iterable[ProcessEffect],
        rng: np.random.Generator,
        noise_std: float = 0.004,
    ):

        self.effects = list(effects)

        self.rng = rng

        self.noise_std = noise_std

    # -------------------------------------------------

    def expected_yield(
        self,
        recipe: Recipe,
        equipment: Equipment,
    ) -> float:

        value = 0.70

        for effect in self.effects:

            value += effect.evaluate(
                recipe,
                equipment,
            )

        return float(
            np.clip(
                value,
                0.0,
                1.0,
            )
        )

    # -------------------------------------------------

    def measure(
        self,
        recipe: Recipe,
        equipment: Equipment,
    ) -> YieldResult:

        expected = self.expected_yield(
            recipe,
            equipment,
        )

        measured = self.rng.normal(
            expected,
            self.noise_std,
        )

        measured = float(
            np.clip(
                measured,
                0.0,
                1.0,
            )
        )

        return YieldResult(

            expected=expected,

            measured=measured,

        )
