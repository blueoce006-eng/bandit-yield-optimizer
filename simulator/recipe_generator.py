"""
recipe_generator.py

Generate semiconductor process recipes.
"""

from __future__ import annotations

from itertools import product

from simulator.recipe import Recipe


class RecipeGenerator:

    def __init__(

        self,

        temperatures,

        pressures,

        rf_powers,

        gas_flows,

    ):

        self.temperatures = temperatures

        self.pressures = pressures

        self.rf_powers = rf_powers

        self.gas_flows = gas_flows

    # --------------------------------------------------

    def generate(self):

        recipes = []

        recipe_id = 0

        for (
            temperature,
            pressure,
            rf,
            gas,
        ) in product(

            self.temperatures,

            self.pressures,

            self.rf_powers,

            self.gas_flows,

        ):

            recipes.append(

                Recipe(

                    name=f"R{recipe_id}",

                    temperature=temperature,

                    pressure=pressure,

                    rf_power=rf,

                    gas_flow=gas,

                )

            )

            recipe_id += 1

        return recipes
