from dataclasses import dataclass


@dataclass(frozen=True)
class Recipe:
    """
    Semiconductor process recipe.

    Attributes
    ----------
    name : str
        Recipe identifier.
    temperature : float
        Chamber temperature (°C).
    pressure : float
        Chamber pressure (Torr).
    rf_power : float
        RF power (W).
    gas_flow : float
        Gas flow (sccm).
    """

    name: str
    temperature: float
    pressure: float
    rf_power: float
    gas_flow: float
