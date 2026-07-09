"""
lot.py

Represents a wafer lot.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from statistics import mean
import uuid
import numpy as np

from simulator.wafer import Wafer


@dataclass(slots=True)
class Lot:
    """
    Semiconductor wafer lot.

    A lot consists of multiple wafers.
    """

    product_type: str

    lot_size: int = 25

    diameter: int = 300

    quality_mean: float = 0.98

    quality_std: float = 0.01

    defect_mean: float = 0.002

    defect_std: float = 0.0005

    rng: np.random.Generator | None = None

    lot_id: str = field(
        default_factory=lambda: str(uuid.uuid4())[:8]
    )

    wafers: list[Wafer] = field(
        init=False,
        default_factory=list,
    )

    # --------------------------------------------------

    def __post_init__(self):

        if self.rng is None:
            self.rng = np.random.default_rng()

        self.wafers = []

        for _ in range(self.lot_size):

            quality = float(
                np.clip(
                    self.rng.normal(
                        self.quality_mean,
                        self.quality_std,
                    ),
                    0.8,
                    1.0,
                )
            )

            defects = max(
                0.0,
                self.rng.normal(
                    self.defect_mean,
                    self.defect_std,
                ),
            )

            wafer = Wafer(

                product_type=self.product_type,

                diameter=self.diameter,

                quality=quality,

                defect_density=defects,

            )

            self.wafers.append(wafer)

    # --------------------------------------------------

    @property
    def average_quality(self) -> float:

        return mean(
            wafer.quality
            for wafer in self.wafers
        )

    # --------------------------------------------------

    @property
    def average_defect_density(self) -> float:

        return mean(
            wafer.defect_density
            for wafer in self.wafers
        )

    # --------------------------------------------------

    @property
    def wafer_count(self):

        return len(self.wafers)

    # --------------------------------------------------

    def __iter__(self):

        return iter(self.wafers)

    # --------------------------------------------------

    def __repr__(self):

        return (
            "Lot("
            f"id={self.lot_id}, "
            f"product={self.product_type}, "
            f"wafers={self.wafer_count}, "
            f"quality={self.average_quality:.3f})"
        )
