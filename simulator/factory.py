from simulator.recipe import Recipe
from simulator.equipment import Equipment
from simulator.yield_model import YieldModel


class Factory:

    def __init__(self, recipes):

        self.recipes = recipes

        self.model = YieldModel()

        self.equipment = Equipment()

        self.day = 0

    def run(self, recipe_id):

        recipe = self.recipes[recipe_id]

        y = self.model.sample(
            recipe,
            self.equipment,
        )

        self.day += 1

        self.equipment.age()

        return y

    def contamination_event(self, severity=0.15):

        self.equipment.contamination += severity

    def maintenance(self):

        self.equipment.clean()
