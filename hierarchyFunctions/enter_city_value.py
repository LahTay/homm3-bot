"""Module containing an algorithm that states the value of entering the city"""
from hierarchyFunctions.power_evaluation import power_evaluation
from data.city import City

def full_unit_cost(town):
    """
    Gives value to the city if there are units to buy

    :param town: Town object
    :return cost: Cost of buying all units
    """
    cost = 0
    if town.t1_generator_lvl.habitat_lvl == 1:
        cost += town.t1_generator_lvl.unit_cost.gold * town.t1_generator_lvl.unit_ready
    if town.t1_generator_lvl.habitat_lvl == 2:
        cost += town.t1_generator_lvl.unit_cost_up.gold * town.t1_generator_lvl.unit_ready

    if town.t2_generator_lvl.habitat_lvl == 1:
        cost += town.t2_generator_lvl.unit_cost.gold * town.t2_generator_lvl.unit_ready
    if town.t2_generator_lvl.habitat_lvl == 2:
        cost += town.t2_generator_lvl.unit_cost_up.gold * town.t2_generator_lvl.unit_ready

    if town.t3_generator_lvl.habitat_lvl == 1:
        cost += town.t3_generator_lvl.unit_cost.gold * town.t3_generator_lvl.unit_ready
    if town.t3_generator_lvl.habitat_lvl == 2:
        cost += town.t3_generator_lvl.unit_cost_up.gold * town.t3_generator_lvl.unit_ready

    if town.t4_generator_lvl.habitat_lvl == 1:
        cost += town.t4_generator_lvl.unit_cost.gold * town.t4_generator_lvl.unit_ready
    if town.t4_generator_lvl.habitat_lvl == 2:
        cost += town.t4_generator_lvl.unit_cost_up.gold * town.t4_generator_lvl.unit_ready

    if town.t5_generator_lvl.habitat_lvl == 1:
        cost += town.t5_generator_lvl.unit_cost.gold * town.t5_generator_lvl.unit_ready
    if town.t5_generator_lvl.habitat_lvl == 2:
        cost += town.t5_generator_lvl.unit_cost_up.gold * town.t5_generator_lvl.unit_ready

    if town.t6_generator_lvl.habitat_lvl == 1:
        cost += town.t6_generator_lvl.unit_cost.gold * town.t6_generator_lvl.unit_ready
    if town.t6_generator_lvl.habitat_lvl == 2:
        cost += town.t6_generator_lvl.unit_cost_up.gold * town.t6_generator_lvl.unit_ready

    if town.t7_generator_lvl.habitat_lvl == 1:
        cost += town.t7_generator_lvl.unit_cost.gold * town.t7_generator_lvl.unit_ready
    if town.t7_generator_lvl.habitat_lvl == 2:
        cost += town.t7_generator_lvl.unit_cost_up.gold * town.t7_generator_lvl.unit_ready
    return cost

# TODO value jesli chcemy uzywac speli

#
# def new_magic(town):
#     """
#
#     :param town:
#     :return True or False:
#     """
#     if town.last_built.name == "Mage_Guild":
#         return True
#     else:
#         return False


def units_up(day):
    """
    Checks if there is a new week

    :param day: Parameter stating the day.
    :return: Boolean. True -> are up. False -> Not up.
    """
    if day == 1:
        return True
    else:
        return False


def enter_city_evaluation(arg, player, hero):
    """
    Adds value to the city

    :param arg: City to evaluate
    :param player: Player instance
    :param hero: Current hero
    :return: Value
    """

    number = 0
    if isinstance(arg, int):
        return 0

    if hero.herotype != 'main':
        return 0

    if issubclass(type(arg), City):
        if arg not in player.cities:  # Add any value to a city that isn't ours
            return 1000

    # wejscie do naszego miasta
    if arg in player.cities and hero.herotype == 'main':
        number = (arg.t1_generator_lvl.unit_type.value * arg.t1_generator_lvl.unit_ready +
                  arg.t2_generator_lvl.unit_type.value * arg.t2_generator_lvl.unit_ready +
                  arg.t3_generator_lvl.unit_type.value * arg.t3_generator_lvl.unit_ready +
                  arg.t4_generator_lvl.unit_type.value * arg.t4_generator_lvl.unit_ready +
                  arg.t5_generator_lvl.unit_type.value * arg.t5_generator_lvl.unit_ready +
                  arg.t6_generator_lvl.unit_type.value * arg.t6_generator_lvl.unit_ready +
                  arg.t7_generator_lvl.unit_type.value * arg.t7_generator_lvl.unit_ready)
        try:
            if player.gold/full_unit_cost(player.cities[0]) >= 1:
                number = number * 1
            elif player.gold/full_unit_cost(player.cities[0]) >= 0.9:
                number = number * 0.9
            elif player.gold/full_unit_cost(player.cities[0]) >= 0.8:
                number = number * 0.8
            elif player.gold/full_unit_cost(player.cities[0]) >= 0.7:
                number = number * 0.7
            elif player.gold/full_unit_cost(player.cities[0]) >= 0.6:
                number = number * 0.6
            elif player.gold/full_unit_cost(player.cities[0]) >= 0.5:
                number = number * 0.5
            elif player.gold/full_unit_cost(player.cities[0]) >= 0.4:
                number = number * 0.4
            else:
                number = 0
        except ZeroDivisionError:
            number = 0
    else:
        number = 0

        # if new_magic(player.cities[0]):
        #     number = number + 400
        # else:
        #     pass

        #wejscie do Neutral / Enemy
        # else:
        #     #TODO dodac miastu Slots
        #     zmienna = power_evaluation(player.heroes, arg.slots)
        #
        #     if zmienna == 1:
        #         number = number + 400
        #     else:
        #         number = number - 5000000


    if player.gold > 15000:
        return number * 2
    else:
        return number

