"""
wafer.py

Represents a wafer entering the fabrication process.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import uuid


@dataclass(slots=True)
class Wafer:
    """
    A semiconductor wafer.

    Parameters
    ----------
    product_type : str
        Product family (e.g. DRAM, NAND).

    diameter : int
        Wafer diameter in mm.

    defect_density : float
        Initial defect density.

    quality : float
        Incoming wafer quality (0~1).
    """

    product_type: str

    diameter: int = 300

    defect_density: float = 0.002

    quality: float = 1.0

    wafer_id: str = field(
        default_factory=lambda: str(uuid.uuid4())[:8]
    )

    def apply_damage(
        self,
        amount: float,
    ) -> None:
        """
        Increase defect density.
        """

        self.defect_density += amount

        self.quality = max(
            0.0,
            self.quality - amount * 20,
        )

    @property
    def defect_factor(self) -> float:
        """
        Multiplicative factor applied to yield.
        """

        return max(
            0.5,
            1.0 - self.defect_density * 10,
        )

    def __repr__(self):

        return (
            f"Wafer("
            f"id={self.wafer_id}, "
            f"type={self.product_type}, "
            f"quality={self.quality:.3f}, "
            f"defects={self.defect_density:.5f})"
        )
