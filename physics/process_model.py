"""
process_model.py

Factory process simulator.

This module evaluates process time, energy,
throughput, revenue, profit and reward.
"""

from __future__ import annotations

from dataclasses import dataclass

from simulator.recipe import Recipe
from simulator.equipment import Equipment

from physics.cost_model import CostResult


# ==========================================================
# Result
# ==========================================================

@dataclass(slots=True)
class ProcessResult:

    cycle_time: float

    energy: float

    throughput: float

    revenue: float

    profit: float

    reward: float


# ==========================================================
# Model
# ==========================================================

class ProcessModel:

    def __init__(

        self,

        wafer_price: float = 100.0,

        reward_cost_weight: float = 1.0,

        reward_time_weight: float = 0.05,

    ):

        self.wafer_price = wafer_price

        self.reward_cost_weight = reward_cost_weight

        self.reward_time_weight = reward_time_weight

    # ------------------------------------------------------

    def cycle_time(

        self,

        recipe: Recipe,

    ) -> float:
        """
        Estimated process time (seconds)
        """

        heating = 40.0

        heating += max(
            0,
            recipe.temperature - 650,
        ) * 0.8

        pressure_delay = abs(
            recipe.pressure - 20
        ) * 2.5

        plasma = recipe.rf_power * 0.05

        gas_delay = recipe.gas_flow * 0.03

        return (

            heating

            + pressure_delay

            + plasma

            + gas_delay

        )

    # ------------------------------------------------------

    def energy(

        self,

        recipe: Recipe,

        cycle_time: float,

    ) -> float:
        """
        Estimated energy consumption (kWh)
        """

        heating = (
            recipe.temperature
            * 0.002
        )

        rf = (
            recipe.rf_power
            * cycle_time
            / 3600
        )

        pump = (
            recipe.pressure
            * 0.05
        )

        return (

            heating

            + rf

            + pump

        )

    # ------------------------------------------------------

    def throughput(

        self,

        cycle_time: float,

    ) -> float:
        """
        Wafers processed per hour.
        """

        return (

            3600

            / cycle_time

        )

    # ------------------------------------------------------

    def revenue(

        self,

        yield_rate: float,

    ) -> float:
        """
        Income from one wafer.
        """

        return (

            yield_rate

            * self.wafer_price

        )

    # ------------------------------------------------------

    def profit(

        self,

        revenue: float,

        cost: CostResult,

    ) -> float:

        return (

            revenue

            - cost.total

        )

    # ------------------------------------------------------

    def reward(

        self,

        profit: float,

        cycle_time: float,

    ) -> float:
        """
        Reward used by Bandit.
        """

        return (

            profit

            - self.reward_time_weight
            * cycle_time

        )

    # ------------------------------------------------------

    def evaluate(

        self,

        recipe: Recipe,

        equipment: Equipment,

        yield_rate: float,

        cost: CostResult,

    ) -> ProcessResult:

        cycle_time = self.cycle_time(
            recipe,
        )

        energy = self.energy(
            recipe,
            cycle_time,
        )

        throughput = self.throughput(
            cycle_time,
        )

        revenue = self.revenue(
            yield_rate,
        )

        profit = self.profit(
            revenue,
            cost,
        )

        reward = self.reward(
            profit,
            cycle_time,
        )

        return ProcessResult(

            cycle_time=cycle_time,

            energy=energy,

            throughput=throughput,

            revenue=revenue,

            profit=profit,

            reward=reward,

        )
