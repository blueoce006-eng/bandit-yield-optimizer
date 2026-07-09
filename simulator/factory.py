"""
factory.py

Semiconductor fabrication environment.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from simulator.recipe import Recipe
from simulator.recipe_generator import RecipeGenerator
from simulator.lot_generator import LotGenerator
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
from physics.simulation_result import SimulationResult


class Factory:
    """
    Semiconductor fabrication simulator.

    Environment for Multi-Armed Bandit algorithms.
    """

    def __init__(
        self,
        seed: int = 42,
        switching_cost: float = 2.0,
    ):

        self.rng = np.random.default_rng(seed)

        self.equipment = Equipment()

        self.recipes = RecipeGenerator(
            temperatures=[640, 650, 660, 670, 680],
            pressures=[18, 20, 22],
            rf_powers=[90, 100, 110],
            gas_flows=[40, 50, 60],
        ).generate()

        self.lot_generator = LotGenerator(
            rng=self.rng
        )

        effects = [

            TemperatureEffect(),

            PressureEffect(),

            RFPowerEffect(),

            GasFlowEffect(),

            TemperaturePressureInteraction(),

            RFGasInteraction(),

            EquipmentEffect(),

        ]

        self.yield_model = YieldModel(

            effects=effects,

            rng=self.rng,

        )

        self.cost_model = CostModel()

        self.process_model = ProcessModel()

        self.switching_cost = switching_cost

        self.previous_arm = None

        self.total_steps = 0

    # -------------------------------------------------

    @property
    def n_arms(self):

        return len(self.recipes)

    # -------------------------------------------------

    def reset(self):

        """
        Reset environment.
        """

        self.equipment = Equipment()

        self.previous_arm = None

        self.total_steps = 0

    # -------------------------------------------------

    def pull_arm(
        self,
        arm: int,
    ) -> SimulationResult:

        recipe = self.recipes[arm]

        lot = self.lot_generator.generate()

        yields = []

        expected = []

        for wafer in lot:

            result = self.yield_model.measure(
                recipe,
                self.equipment,
            )

            y = (
                result.measured
                * wafer.quality
                * wafer.defect_factor
            )

            y = float(
                np.clip(
                    y,
                    0.0,
                    1.0,
                )
            )

            yields.append(y)

            expected.append(result.expected)

            self.equipment.process_wafer(
                recipe
            )

        lot_yield = float(np.mean(yields))

        expected_yield = float(
            np.mean(expected)
        )

        cost = self.cost_model.evaluate(
            recipe,
            self.equipment,
        )

        process = self.process_model.evaluate(

            recipe,

            self.equipment,

            yield_rate=lot_yield,

            cost=cost,

        )

        switching = 0.0

        if (
            self.previous_arm is not None
            and self.previous_arm != arm
        ):
            switching = self.switching_cost

        reward = (
            process.reward
            - switching
        )

        self.previous_arm = arm

        self.total_steps += 1

        return SimulationResult(

            recipe=recipe,

            arm_id=arm,

            lot_id=lot.lot_id,

            expected_yield=expected_yield,

            measured_yield=lot_yield,

            lot_yield=lot_yield,

            wafers_processed=lot.wafer_count,

            cycle_time=process.cycle_time,

            throughput=process.throughput,

            energy=process.energy,

            process_cost=cost.total,

            revenue=process.revenue,

            profit=process.profit,

            switching_cost=switching,

            reward=reward,

            equipment_health=self.equipment.health,

            contamination=self.equipment.contamination,

            maintenance_required=self.equipment.requires_maintenance,

            event=None,

        )
