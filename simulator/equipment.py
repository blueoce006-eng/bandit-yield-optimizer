"""
equipment.py

Equipment state model for the virtual semiconductor fabrication simulator.
"""

from __future__ import annotations

from dataclasses import dataclass

from simulator.recipe import Recipe


@dataclass(slots=True)
class Equipment:
    """
    Represents a fabrication tool.

    The equipment gradually degrades as wafers are processed.

    Attributes
    ----------
    health
        Overall machine health (0~1).

    contamination
        Particle contamination level (0~1).

    processed_wafers
        Total number of processed wafers.

    maintenance_count
        Number of maintenance operations.
    """

    health: float = 1.0

    contamination: float = 0.0

    processed_wafers: int = 0

    maintenance_count: int = 0

    base_wear: float = 1e-5

    def process_wafer(self, recipe: Recipe) -> None:
        """
        Update equipment condition after processing one wafer.
        """

        self.processed_wafers += 1

        wear = self.base_wear

        # ---------- Temperature ----------

        wear += max(
            0.0,
            recipe.temperature - 650
        ) * 2e-7

        # ---------- RF Power ----------

        wear += max(
            0.0,
            recipe.rf_power - 90
        ) * 1e-7

        # ---------- Gas ----------

        wear += recipe.gas_flow * 2e-8

        self.health = max(
            0.80,
            self.health - wear,
        )

        # ---------- Contamination ----------

        contamination_gain = (
            1e-6
            * recipe.pressure
            * recipe.gas_flow
        )

        self.contamination = min(
            0.30,
            self.contamination + contamination_gain,
        )

    def contamination_event(
        self,
        severity: float,
    ) -> None:
        """
        Unexpected particle contamination.
        """

        self.contamination = min(
            1.0,
            self.contamination + severity,
        )

    def clean(self) -> None:
        """
        Chamber cleaning.
        """

        self.contamination *= 0.1

    def maintenance(self) -> None:
        """
        Restore equipment condition.
        """

        self.health = 1.0

        self.contamination = 0.0

        self.maintenance_count += 1

    @property
    def efficiency(self) -> float:
        """
        Overall equipment efficiency.
        """

        efficiency = (
            self.health
            * (1.0 - self.contamination)
        )

        return max(
            0.0,
            min(1.0, efficiency),
        )

    @property
    def requires_maintenance(self) -> bool:
        """
        Indicates whether preventive maintenance
        should be considered.
        """

        return (
            self.health < 0.90
            or self.contamination > 0.15
        )

    def __repr__(self):

        return (
            "Equipment("
            f"health={self.health:.4f}, "
            f"contamination={self.contamination:.4f}, "
            f"efficiency={self.efficiency:.4f}, "
            f"processed={self.processed_wafers})"
        )
