"""
lot_generator.py

Generate semiconductor lots.
"""

from __future__ import annotations

import numpy as np

from simulator.lot import Lot


class LotGenerator:

    def __init__(

        self,

        rng: np.random.Generator,

        lot_size: int = 25,

        product_type: str = "DRAM",

    ):

        self.rng = rng

        self.lot_size = lot_size

        self.product_type = product_type

    def generate(self) -> Lot:

        quality_mean = self.rng.normal(

            loc=0.98,

            scale=0.005,

        )

        defect_mean = self.rng.normal(

            loc=0.002,

            scale=0.0002,

        )

        return Lot(

            product_type=self.product_type,

            lot_size=self.lot_size,

            quality_mean=float(quality_mean),

            defect_mean=float(defect_mean),

            rng=self.rng,

        )
