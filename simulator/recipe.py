"""
recipe.py

Defines a semiconductor process recipe.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Recipe:
    """
    Immutable semiconductor process recipe.

    Parameters
    ----------
    name : str
        Recipe identifier.

    temperature : float
        Process temperature (°C)

    pressure : float
        Chamber pressure (Torr)

    rf_power : float
        RF Power (W)

    gas_flow : float
        Gas Flow (sccm)
    """

    name: str

    temperature: float

    pressure: float

    rf_power: float

    gas_flow: float

    @property
    def features(self) -> tuple[float, float, float, float]:
        """
        Returns process parameters.
        """

        return (
            self.temperature,
            self.pressure,
            self.rf_power,
            self.gas_flow,
        )

    def __repr__(self):

        return (
            f"Recipe("
            f"{self.name}, "
            f"T={self.temperature}, "
            f"P={self.pressure}, "
            f"RF={self.rf_power}, "
            f"Gas={self.gas_flow})"
        )
