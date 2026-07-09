"""
cost_model.py

Cost model for the semiconductor process simulator.
"""

from __future__ import annotations

from dataclasses import dataclass

from simulator.recipe import Recipe
from simulator.equipment import Equipment


# =====================================================
# Cost Result
# =====================================================

@dataclass(slots=True)
class CostResult:
    """
    Detailed cost breakdown.
    """

    heating: float

    rf_power: float

    gas: float

    wear: float

    maintenance: float

    total: float


# =====================================================
# Cost Model
# =====================================================

class CostModel:

    def __init__(

        self,

        electricity_price: float = 0.18,

        gas_price: float = 0.06,

        maintenance_factor: float = 5.0,

    ):

        self.electricity_price = electricity_price

        self.gas_price = gas_price

        self.maintenance_factor = maintenance_factor

    # -------------------------------------------------

    def heating_cost(
        self,
        recipe: Recipe,
    ) -> float:

        return (

            40

            + (recipe.temperature - 650)

            * 0.4

        ) * self.electricity_price

    # -------------------------------------------------

    def rf_cost(
        self,
        recipe: Recipe,
    ) -> float:

        return (

            recipe.rf_power

            * 0.12

        ) * self.electricity_price

    # -------------------------------------------------

    def gas_cost(
        self,
        recipe: Recipe,
    ) -> float:

        return (

            recipe.gas_flow

            * self.gas_price

        )

    # -------------------------------------------------

    def wear_cost(

        self,

        equipment: Equipment,

    ) -> float:

        degradation = (

            1.0

            - equipment.health

        )

        return (

            degradation

            * self.maintenance_factor

        )

    # -------------------------------------------------

    def maintenance_cost(

        self,

        equipment: Equipment,

    ) -> float:

        return (

            equipment.maintenance_count

            * 0.5

        )

    # -------------------------------------------------

    def evaluate(

        self,

        recipe: Recipe,

        equipment: Equipment,

    ) -> CostResult:

        heating = self.heating_cost(recipe)

        rf = self.rf_cost(recipe)

        gas = self.gas_cost(recipe)

        wear = self.wear_cost(equipment)

        maintenance = self.maintenance_cost(equipment)

        total = (

            heating

            + rf

            + gas

            + wear

            + maintenance

        )

        return CostResult(

            heating=heating,

            rf_power=rf,

            gas=gas,

            wear=wear,

            maintenance=maintenance,

            total=total,

        )
