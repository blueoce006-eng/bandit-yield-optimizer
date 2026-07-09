"""
factory.py

Virtual semiconductor fabrication factory.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from simulator.recipe import Recipe
from simulator.equipment import Equipment

from physics.effects import (
    TemperatureEffect,
    PressureEffect,
    RFPowerEffect,
    GasFlowEffect,
    TemperaturePressureInteraction,
    RFGasInteraction,
    EquipmentEffect,
)

from physics.yield_model import YieldModel
from physics.cost_model import CostModel
from physics.process_model import ProcessModel


# ==========================================================
# Factory Result
# ==========================================================

@dataclass(slots=True)
class FactoryResult:

    recipe: Recipe

    yield_rate: float

    expected_yield: float

    process_cost: float

    cycle_time: float

    energy: float

    throughput: float

    revenue: float

    profit: float

    reward: float


# ==========================================================
# Factory
# ==========================================================

class Factory:

    def __init__(

        self,

        seed: int = 42,

    ):

        rng = np.random.default_rng(seed)

        self.equipment = Equipment()

        self.yield_model = YieldModel(

            rng=rng,

            effects=[

                TemperatureEffect(),

                PressureEffect(),

                RFPowerEffect(),

                GasFlowEffect(),

                TemperaturePressureInteraction(),

                RFGasInteraction(),

                EquipmentEffect(),

            ],

        )

        self.cost_model = CostModel()

        self.process_model = ProcessModel()

    # -----------------------------------------------------

    def produce(

        self,

        recipe: Recipe,

    ) -> FactoryResult:

        # Yield

        yield_result = self.yield_model.measure(

            recipe,

            self.equipment,

        )

        # Cost

        cost = self.cost_model.evaluate(

            recipe,

            self.equipment,

        )

        # Process

        process = self.process_model.evaluate(

            recipe,

            self.equipment,

            yield_rate=yield_result.measured,

            cost=cost,

        )

        # Equipment degradation

        self.equipment.process_wafer(

            recipe,

        )

        return FactoryResult(

            recipe=recipe,

            yield_rate=yield_result.measured,

            expected_yield=yield_result.expected,

            process_cost=cost.total,

            cycle_time=process.cycle_time,

            energy=process.energy,

            throughput=process.throughput,

            revenue=process.revenue,

            profit=process.profit,

            reward=process.reward,

        )

    # -----------------------------------------------------

    def maintenance(self):

        self.equipment.maintenance()

    # -----------------------------------------------------

    def contamination(

        self,

        severity: float,

    ):

        self.equipment.contamination_event(

            severity,

        )

    # -----------------------------------------------------

    def reset(

        self,

    ):

        self.equipment = Equipment()
