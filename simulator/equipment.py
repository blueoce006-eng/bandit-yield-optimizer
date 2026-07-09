from dataclasses import dataclass


@dataclass
class Equipment:
    """
    Represents equipment health.
    """

    health: float = 1.0
    contamination: float = 0.0

    def age(self, amount: float = 0.0001):
        """
        Equipment slowly degrades.
        """
        self.health = max(0.8, self.health - amount)

    def clean(self):
        """
        Maintenance.
        """
        self.contamination = 0.0
        self.health = 1.0
