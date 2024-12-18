"""Script containing Cost and building class along with classes inheriting after building class"""

from data.creature import Creature
from data.magic import Spells


class Cost:
    def __init__(self, gold: int, wood: int, ore: int, mercury: int, sulfur: int, crystal: int, gems: int):
        """
        Class representing cost (in resources).

        :param gold: Amount of gold
        :param wood: Amount of wood
        :param ore: Amount of ore
        :param mercury: Amount of mercury
        :param sulfur: Amount of sulfur
        :param crystal: Amount of crystal
        :param gems: Amount of gems
        """
        self.gold = gold
        self.wood = wood
        self.ore = ore
        self.mercury = mercury
        self.sulfur = sulfur
        self.crystal = crystal
        self.gems = gems
        self.resources = [self.gold, self.wood, self.ore, self.mercury, self.sulfur, self.crystal, self.gems]


class Building:
    def __init__(self, name: str, x: int, y: int, x2: int, y2: int, built: bool = False, *cost: Cost):
        """
        Class representing Building (f.e MageGuild..)

        :param name: Name of the object
        :param x: Building "x" location in the city view
        :param y: Building "y" location in the city view
        :param x2: Building "x" location in city hall
        :param y2: Building "y" location in city hall
        :param built: boolean. built -> True, not built -> False
        :param cost: Construction cost of the building
        """
        self.name = name
        self.built = built
        self.position = (x, y)
        self.cost = cost
        self.to_build = (x2, y2)


class MageGuild(Building):
    def __init__(self, lvl: int, name: str, spells: Spells, *cost: Cost, x: int = 0, y: int = 0, x2: int = 0,
                 y2: int = 0, built: bool = False):
        """
        Class Inheriting after building class. Representing Mage Guild building.

        :param lvl: Mage guild level
        :param name: Name of the building
        :param spells: Spells present in mage guild
        :param cost: Construction cost of the building
        :param x: Building "x" location in the city view
        :param y: Building "y" location in the city view
        :param x2: Building "x" location in city hall
        :param y2: Building "y" location in city hall
        :param built: boolean. built -> True, not built -> False
        """
        super().__init__(name, x, y, x2, y2, built, *cost)
        self.mage_guild_lvl = lvl
        self.spells = spells


class Fort(Building):
    def __init__(self, lvl: int = 0, name: str = "Fort", x: int = 0, y: int = 0, x2: int = 0, y2: int = 0, built=False,
                 *cost: Cost,
                 xh1: int = 650, yh1: int = 200, xh2: int = 1300, yh2: int = 200, xh3: int = 650, yh3: int = 400,
                 xh4: int = 1300, yh4: int = 400, xh5: int = 650, yh5: int = 600, xh6: int = 1300, yh6: int = 600,
                 xh7: int = 1000, yh7: int = 800):
        """
        Class Inheriting after building class. Representing Fort building.

        :param lvl: Fort level
        :param name: Name of the building
        :param x: Building "x" location in the city view
        :param y: Building "y" location in the city view
        :param x2: Building "x" location in city hall
        :param y2: Building "y" location in city hall
        :param built: boolean. built -> True, not built -> False
        :param cost: Construction cost of the building
        """
        super().__init__(name, x, y, x2, y2, built, *cost)
        self.fort_lvl = lvl
        self.h1_position = (xh1, yh1)
        self.h2_position = (xh2, yh2)
        self.h3_position = (xh3, yh3)
        self.h4_position = (xh4, yh4)
        self.h5_position = (xh5, yh5)
        self.h6_position = (xh6, yh6)
        self.h7_position = (xh7, yh7)


class CityHall(Building):
    def __init__(self, lvl: int = 0, name: str = '', x: int = 0, y: int = 0, x2: int = 0, y2: int = 0,
                 built: bool = False, *cost: Cost, income: int = 500):
        """
        Class inheriting after building class. Representing City Hall building.

        :param lvl: Mage guild level
        :param name: Name of the building
        :param cost: Construction cost of the building
        :param x: Building "x" location in the city view
        :param y: Building "y" location in the city view
        :param x2: Building "x" location in city hall
        :param y2: Building "y" location in city hall
        :param built: boolean. built -> True, not built -> False
        :param income: Amount of gold received from the City Hall object
        """
        super().__init__(name, x, y, x2, y2, built, *cost)
        self.city_hall_lvl = lvl
        self.income = income


class Tavern(Building):
    def __init__(self, name: str = '', x: int = 0, y: int = 0, x2: int = 0, y2: int = 0, built: bool = False,
                 *cost: Cost,
                 h1x: int = 800, h1y: int = 700, h2x: int = 950, h2y: int = 700):
        """
        Class inheriting after building class. Representing Tavern building.

        :param name: Name of the building
        :param x: Building "x" location in the city view
        :param y: Building "y" location in the city view
        :param x2: Building "x" location in city hall
        :param y2: Building "y" location in city hall
        :param built: boolean. built -> True, not built -> False
        :param cost: Construction cost of the building
        :param h1x: "x" location of 1st hero
        :param h1y: "y" location of 1st hero
        :param h2x: "x" location of 2st hero
        :param h2y: "y" location of 2st hero
        """
        super().__init__(name, x, y, x2, y2, built, *cost)
        self.h1_position = (h1x, h1y)
        self.h2_position = (h2x, h2y)


class Marketplace(Building):
    def __init__(self, name: str = '', x: int = 0, y: int = 0, x2: int = 0, y2: int = 0, built: bool = False,
                 *cost: Cost):
        """
        Class inheriting after building class. Representing Marketplace building.

        :param name: Name of the building
        :param x: Building "x" location in the city view
        :param y: Building "y" location in the city view
        :param x2: Building "x" location in city hall
        :param y2: Building "y" location in city hall
        :param built: boolean. built -> True, not built -> False
        :param cost: Construction cost of the building
        """
        super().__init__(name, x, y, x2, y2, built, *cost)


class ResourceSilo(Building):
    def __init__(self, name: str = '', x: int = 0, y: int = 0, x2: int = 0, y2: int = 0, built: bool = False,
                 *cost: Cost, income: Cost):
        """
        Class inheriting after building class. Representing Resource Silo building.

        :param name: Name of the building
        :param x: Building "x" location in the city view
        :param y: Building "y" location in the city view
        :param x2: Building "x" location in city hall
        :param y2: Building "y" location in city hall
        :param built: boolean. built -> True, not built -> False
        :param cost: Construction cost of the building
        :param income: Amount of gold received from the Resource Silo object
        """
        super().__init__(name, x, y, x2, y2, built, *cost)
        self.income = income


class Habitat(Building):
    def __init__(self, cost: (Cost, Cost), unit: Creature, unit_up: Creature, growth: int,
                 unit_cost: Cost, unit_cost_up: Cost, to_buy: int = 0, lvl: int = 0,
                 name: str = '', x: int = 0, y: int = 0, x2: int = 0, y2: int = 0, built: bool = False):
        """
        Class inheriting after building class. Representing Habitat building.

        :param cost: Construction cost of the building
        :param unit: Which unit does the habitat produce
        :param unit_up: Which upgraded unit does the habitat produce
        :param growth: Unit growth per week
        :param unit_cost: Cost of the unit
        :param unit_cost_up: Cost of the upgraded unit
        :param to_buy: How many units is available to buy
        :param lvl: Habitat level
        :param name: Name of the building
        :param cost: Construction cost of the building
        :param x: Building "x" location in the city view
        :param y: Building "y" location in the city view
        :param x2: Building "x" location in city hall
        :param y2: Building "y" location in city hall
        :param built: boolean. built -> True, not built -> False
        """
        super().__init__(name, x, y, x2, y2, built, cost)
        self.habitat_lvl = lvl
        self.unit_type = unit
        self.unit_type_up = unit_up
        self.growth = growth
        self.unit_cost = unit_cost
        self.unit_cost_up = unit_cost_up
        self.unit_ready = growth
