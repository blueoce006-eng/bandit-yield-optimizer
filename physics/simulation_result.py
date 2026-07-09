"""
simulation_result.py

Data structures returned by the semiconductor simulator.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from simulator.recipe import Recipe


@dataclass(slots=True)
class SimulationResult:
    """
    Final result of processing one lot.

    This object is returned by Factory.pull_arm()
    and consumed by the Bandit algorithms.
    """

    # --------------------------
    # Metadata
    # --------------------------

    recipe: Recipe

    lot_id: str

    arm_id: int

    # --------------------------
    # Yield
    # --------------------------

    expected_yield: float

    measured_yield: float

    lot_yield: float

    # --------------------------
    # Production
    # --------------------------

    wafers_processed: int

    cycle_time: float

    throughput: float

    # --------------------------
    # Economics
    # --------------------------

    energy: float

    process_cost: float

    revenue: float

    profit: float

    switching_cost: float

    reward: float

    # --------------------------
    # Equipment
    # --------------------------

    equipment_health: float

    contamination: float

    maintenance_required: bool

    # --------------------------
    # Optional event
    # --------------------------

    event: Optional[str] = None
