

def town_choice(player, town):
    """
    This function is used in upgrading of all towns. It tells our bot what buildings it can upgrade and when

    :param player:
    :param town: The city that is being upgraded
    :return: boolean variables which correspond to the type of building we want to upgrade
    """
    if player.gold > 20000 and player.wood > 20 and player.ore > 20 and player.mercury > 20 and player.sulfur > 20 and player.crystal > 20 and player.gems > 20:
        return True, True, True, True, True, True

    build_habitat = habitat(town)
    build_fort = fort(player.day, player.daily_income)
    build_cityhall = city_hall(town, player.day)
    build_M_MG_B = MG(town)
    upgrade_habitat = upgrade(town)
    buildings = other(town,player)

    return build_habitat, upgrade_habitat, build_fort, build_cityhall, build_M_MG_B, buildings


def full_unit_cost(town):
    """
    function that checks the max cost of all units that we are able to buy in a week without the cos of not bought units.

    :param town: Town in which we want to buy units
    :return: cost of units
    """
    cost = 0
    if town.t1_generator_lvl.habitat_lvl>0:
        cost += town.t1_generator_lvl.unit_cost.gold * town.t1_generator_lvl.growth
    if town.t2_generator_lvl.habitat_lvl>0:
        cost += town.t2_generator_lvl.unit_cost.gold * town.t2_generator_lvl.growth
    if town.t3_generator_lvl.habitat_lvl>0:
        cost += town.t3_generator_lvl.unit_cost.gold * town.t3_generator_lvl.growth
    if town.t4_generator_lvl.habitat_lvl>0:
        cost += town.t4_generator_lvl.unit_cost.gold * town.t4_generator_lvl.growth
    if town.t5_generator_lvl.habitat_lvl>0:
        cost += town.t5_generator_lvl.unit_cost.gold * town.t5_generator_lvl.growth
    if town.t6_generator_lvl.habitat_lvl>0:
        cost += town.t6_generator_lvl.unit_cost.gold * town.t6_generator_lvl.growth
    if town.t7_generator_lvl.habitat_lvl>0:
        cost += town.t7_generator_lvl.unit_cost.gold * town.t7_generator_lvl.growth
    return cost


def city_hall(town, day):
    """
    function created to make decision whether we want to upgrade city hall or not. Possible extension of the function

    :param town:
    :param day:
    :return: boolean variable
    """
    return True


def habitat(town):
    """
    This function tells us whether we want to buy next dwelling or not.

    :param town: Town being upgraded
    :return: boolean variable
    """
    if town.city_hall.city_hall_lvl == 2 and town.fort.fort_lvl == 3:
        return False
    else:
        return True


def fort(day, income):
    """
    This function tells us whether we want to upgrade our fort or not

    :param day: day of the week
    :param income: player income
    :return: boolean variable
    """
    if day >= 5:
        if income[2] != 0:
            return True
        else:
            return False
    else:
        return False


def MG(town):
    """
    This function tells us whether we want to upgrade Mage Guild or not

    :param town: Town being upgraded
    :return: boolean variable
    """
    if town.city_hall.city_hall_lvl >= 1:
        return True
    else:
        return False


def other(town, player):
    """
    This function tells us whether we want to upgrade buildings like (Blacksmith, market...)

    :param town: Town being upgrade
    :return: boolean variable
    """
    if town.city_hall.city_hall_lvl >= 2 and player.gold > 7000:
        return True
    else:
        return False


def upgrade(town):
    """
    This function tells us whether we want to upgrade our dwellings or not.

    :param town: Town being upgraded
    :return: boolean variable
    """
    if town.city_hall.city_hall_lvl >= 2:
        # return False
        return True
    else:
        return False
