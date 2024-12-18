"""Script containing Stronghold castle upgrade alghoritm"""
from town_upgrading.choice_generator import *
from GUI_handling.TownGUI import buy_building


def resourceCheck(buildingCost, playerRsrc):
    """
    Checks if a player has enough resources to build.
    :param buildingCost: Cost of the given building
    :param playerRsrc: Resources of the player
    :return: true or false
    """
    if (playerRsrc.gold >= buildingCost.gold) and (playerRsrc.wood >= buildingCost.wood) and (
            playerRsrc.ore >= buildingCost.ore) and (playerRsrc.mercury >= buildingCost.mercury) and (
            playerRsrc.sulfur >= buildingCost.sulfur) and (playerRsrc.crystal >= buildingCost.crystal) and (
            playerRsrc.gems >= buildingCost.gems):
        return True
    else:
        return False


def build(buildingCost, playerRsrc):
    """
    Functions responsible for building and managing resources after construction
    :param buildingCost: Cost of the given building
    :param playerRsrc: Resources of the player
    """
    playerRsrc.gold -= buildingCost.gold
    playerRsrc.wood -= buildingCost.wood
    playerRsrc.ore -= buildingCost.ore
    playerRsrc.mercury -= buildingCost.mercury
    playerRsrc.sulfur -= buildingCost.sulfur
    playerRsrc.crystal -= buildingCost.crystal
    playerRsrc.gems -= buildingCost.gems


def strongholdUpgrade(player, stronghold):
    """
    Stronghold castle upgrade alghoritm.
    :param player: Player object
    :param stronghold: Stronghold object
    :return: None
    """
    cost = full_unit_cost(stronghold)
    if player.gold < (cost/3):
        print("Not enought gold for units, dont build anything")
        return None
    # ----------------------------HARDCODED ZONE-----------------------------------------------
    # Tavern
    if stronghold.tavern.built == False:
        if resourceCheck(stronghold.tavern.cost[0], player):
            build(stronghold.tavern.cost[0], player)
            stronghold.tavern.built = True
            buy_building(stronghold.tavern.name, "stronghold")
            print('Tavern built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # Fort
    if stronghold.fort.fort_lvl == 0 and stronghold.tavern.built:
        if resourceCheck(stronghold.fort.cost[0][0], player):
            build(stronghold.fort.cost[0][0], player)
            stronghold.fort.fort_lvl = 1
            buy_building(stronghold.fort.name, "stronghold")
            print('Fort lvl 1 built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # Goblin Barracks
    if not stronghold.t1_generator_lvl.habitat_lvl==0 and stronghold.fort.built:
        if resourceCheck(stronghold.t1_generator_lvl.cost[0][0], player):
            build(stronghold.t1_generator_lvl.cost[0][0], player)
            stronghold.t1_generator_lvl.habitat_lvl=1
            buy_building(stronghold.t1_generator_lvl.name, "stronghold")
            print('Goblin Barracks built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # Wolf Pen
    if stronghold.t1_generator_lvl.habitat_lvl>=1 and stronghold.t2_generator_lvl.habitat_lvl==0:
        if resourceCheck(stronghold.t2_generator_lvl.cost[0][0], player):
            build(stronghold.t2_generator_lvl.cost[0][0], player)
            stronghold.t2_generator_lvl.habitat_lvl=1
            buy_building(stronghold.t2_generator_lvl.name, "stronghold")
            print('Wolf Pen built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # Cliff Nest
    if stronghold.t2_generator_lvl.habitat_lvl>=1 and stronghold.t5_generator_lvl.habitat_lvl==0:
        if resourceCheck(stronghold.t5_generator_lvl.cost[0][0], player):
            build(stronghold.t5_generator_lvl.cost[0][0], player)
            stronghold.t5_generator_lvl.habitat_lvl=1
            buy_building(stronghold.t5_generator_lvl.name, "stronghold")
            print('Cliff Nest built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # Behemoth Lair
    if stronghold.t5_generator_lvl.habitat_lvl>=1 and stronghold.t7_generator_lvl.habitat_lvl==0:
        if resourceCheck(stronghold.t7_generator_lvl.cost[0][0], player):
            build(stronghold.t7_generator_lvl.cost[0][0], player)
            stronghold.t7_generator_lvl.habitat_lvl=1
            buy_building(stronghold.t7_generator_lvl.name, "stronghold")
            print('Behemoth Lair built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # Orc Tower
    if stronghold.t7_generator_lvl.habitat_lvl>=1 and stronghold.t3_generator_lvl.habitat_lvl==0:
        if resourceCheck(stronghold.t3_generator_lvl.cost[0][0], player):
            build(stronghold.t3_generator_lvl.cost[0][0], player)
            stronghold.t3_generator_lvl.habitat_lvl=1
            buy_building(stronghold.t3_generator_lvl.name, "stronghold")
            print('Orc Tower built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # Town Hall
    if stronghold.t3_generator_lvl.habitat_lvl>=1 and stronghold.city_hall.city_hall_lvl==0:
        if resourceCheck(stronghold.city_hall.cost[0][0], player):
            build(stronghold.city_hall.cost[0][0], player)
            stronghold.city_hall.city_hall_lvl = 1
            player.daily_income[0] += 500
            buy_building(stronghold.city_hall.name, "stronghold")
            print('City Hall built!')
            return None
        else:
            print('Not enough resources!')
            return None
    # ----------------------------HARDCODED ZONE-----------------------------------------------
    # [hab = build habitat], [upg = upgrade habitat], [wall = build/upgrade fort], [capi = build/upgrade city_hall], [MG_M = build Marketplace , upgrade/build mage_guild, build blacksmith], [builds = build other buildings]
    hab, upg, wall, capi, MG_M, builds = town_choice(player, stronghold)

    # ------------------------------------------------------------------------------------------
    # Mage guild Level 1
    if stronghold.mage_guild.mage_guild_lvl==0 and MG_M:
        if resourceCheck(stronghold.mage_guild.cost[0][0], player):
            build(stronghold.mage_guild.cost[0][0], player)
            stronghold.mage_guild.mage_guild_lvl = 1
            buy_building(stronghold.mage_guild.name, "stronghold")
            print('Mage guild Level 1!')
            return None
        else:
            print('Not enough resources!')

    # Marketplace
    if not stronghold.marketplace.built and MG_M:
        if resourceCheck(stronghold.marketplace.cost[0], player):
            build(stronghold.marketplace.cost[0], player)
            stronghold.marketplace.built = True
            buy_building(stronghold.marketplace.name, "stronghold")
            print('Marketplace built!')
            return None
        else:
            print('Not enough resources!')

    # Blacksmith
    if not stronghold.blacksmith.built and MG_M:
        if resourceCheck(stronghold.blacksmith.cost[0], player):
            build(stronghold.blacksmith.cost[0], player)
            stronghold.blacksmith.built = True
            buy_building(stronghold.blacksmith.name, "stronghold")
            print('Blacksmith built!')
            return None
        else:
            print('Not enough resources!')

    # City Hall
    if stronghold.blacksmith.built and stronghold.city_hall.city_hall_lvl == 1 and stronghold.mage_guild.mage_guild_lvl>=1 and stronghold.marketplace.built and capi:
        if resourceCheck(stronghold.city_hall.cost[0][1], player):
            build(stronghold.city_hall.cost[0][1], player)
            stronghold.city_hall.city_hall_lvl = 2
            player.daily_income[0] += 1000
            buy_building(stronghold.city_hall.name, "stronghold")
            print('City Hall built!')
            return None
        else:
            print('Not enough resources!')

    # Citadel
    if stronghold.fort.fort_lvl == 1 and wall:
        if resourceCheck(stronghold.fort.cost[0][1], player):
            build(stronghold.fort.cost[0][1], player)
            stronghold.fort.fort_lvl = 2
            buy_building(stronghold.fort.name, "stronghold")
            print('Citadel built!')
            return None
        else:
            print('Not enough resources!')

    # Ogre Fort
    if stronghold.t3_generator_lvl.habitat_lvl>=1 and stronghold.t4_generator_lvl.habitat_lvl==0 and hab:
        if resourceCheck(stronghold.t4_generator_lvl.cost[0][0], player):
            build(stronghold.t4_generator_lvl.cost[0][0], player)
            stronghold.t4_generator_lvl.habitat_lvl=1
            buy_building(stronghold.t4_generator_lvl.name, "stronghold")
            print('Ogre Fort built!')
            return None
        else:
            print('Not enough resources!')

    # Castle
    if stronghold.fort.fort_lvl == 2 and wall:
        if resourceCheck(stronghold.fort.cost[0][2], player):
            build(stronghold.fort.cost[0][2], player)
            stronghold.fort.fort_lvl = 3
            buy_building(stronghold.fort.name, "stronghold")
            print('Castle built!')
            return None
        else:
            print('Not enough resources!')

    # Capitol
    if stronghold.fort.fort_lvl == 3 and stronghold.city_hall.city_hall_lvl == 2 and capi:
        if resourceCheck(stronghold.city_hall.cost[0][2], player):
            build(stronghold.city_hall.cost[0][2], player)
            stronghold.city_hall.city_hall_lvl = 3
            player.daily_income[0] += 2000
            buy_building(stronghold.city_hall.name, "stronghold")
            print('Capitol built!')
            return None
        else:
            print('Not enough resources!')

    # Upg. Orc Tower
    if stronghold.t3_generator_lvl.habitat_lvl==1 and stronghold.blacksmith.built and upg:
        if resourceCheck(stronghold.t3_generator_lvl.cost[0][1], player):
            build(stronghold.t3_generator_lvl.cost[0][1], player)
            stronghold.t3_generator_lvl.habitat_lvl=2
            buy_building(stronghold.t3_generator_lvl.name, "stronghold")
            print('Orc Tower upgraded!')
            return None
        else:
            print('Not enough resources!')

    # Hall of Valhalla
    if not stronghold.hall_of_valhalla.built and stronghold.fort.fort_lvl >= 1 and builds:
        if resourceCheck(stronghold.hall_of_valhalla.cost[0], player):
            build(stronghold.hall_of_valhalla.cost[0], player)
            stronghold.hall_of_valhalla.built = True
            buy_building(stronghold.hall_of_valhalla.name, "stronghold")
            print('Hall of Valhalla built!')
            return None
        else:
            print('Not enough resources!')

    # Upg. Goblin Barracks
    if stronghold.t1_generator_lvl.habitat_lvl==1 and upg:
        if resourceCheck(stronghold.t1_generator_lvl.cost[0][1], player):
            build(stronghold.t1_generator_lvl.cost[0][1], player)
            stronghold.t1_generator_lvl.habitat_lvl=2
            buy_building(stronghold.t1_generator_lvl.name, "stronghold")
            print('Goblin Barracks upgraded!')
            return None
        else:
            print('Not enough resources!')

    # Upg. Wolf Pen
    if stronghold.t1_generator_lvl.habitat_lvl==2 and stronghold.t2_generator_lvl.habitat_lvl==1 and upg:
        if resourceCheck(stronghold.t2_generator_lvl.cost[0][1], player):
            build(stronghold.t2_generator_lvl.cost[0][1], player)
            stronghold.t2_generator_lvl.habitat_lvl=2
            buy_building(stronghold.t2_generator_lvl.name, "stronghold")
            print('Wolf Pen upgraded!')
            return None
        else:
            print('Not enough resources!')

    # Upg. Cliff Nest
    if stronghold.t5_generator_lvl.habitat_lvl==1 and upg:
        if resourceCheck(stronghold.t5_generator_lvl.cost[0][1], player):
            build(stronghold.t5_generator_lvl.cost[0][1], player)
            stronghold.t5_generator_lvl.habitat_lvl=2
            buy_building(stronghold.t5_generator_lvl.name, "stronghold")
            print('Cliff Nest upgraded!')
            return None
        else:
            print('Not enough resources!')

    # Upg. Ogre Fort
    if stronghold.t4_generator_lvl.habitat_lvl==1 and stronghold.mage_guild.mage_guild_lvl>=1 and upg:
        if resourceCheck(stronghold.t4_generator_lvl.cost[0][1], player):
            build(stronghold.t4_generator_lvl.cost[0][1], player)
            stronghold.t4_generator_lvl.habitat_lvl=2
            buy_building(stronghold.t4_generator_lvl.name, "stronghold")
            print('Ogre Fort upgraded!')
            return None
        else:
            print('Not enough resources!')

    # Mage guild Level 2
    if stronghold.mage_guild.mage_guild_lvl == 1 and MG_M:
        if resourceCheck(stronghold.mage_guild.cost[0][1], player):
            build(stronghold.mage_guild.cost[0][1], player)
            stronghold.mage_guild.mage_guild_lvl = 2
            buy_building(stronghold.mage_guild.name, "stronghold")
            print('Mage guild Level 2!')
            return None
        else:
            print('Not enough resources!')

    # Mage guild Level 3
    if stronghold.mage_guild.mage_guild_lvl == 2 and MG_M:
        if resourceCheck(stronghold.mage_guild.cost[0][2], player):
            build(stronghold.mage_guild.cost[0][2], player)
            stronghold.mage_guild.mage_guild_lvl = 3
            buy_building(stronghold.mage_guild.name, "stronghold")
            print('Mage guild Level 3!')
            return None
        else:
            print('Not enough resources!')

    # Upg. Behemoth
    if stronghold.t7_generator_lvl.habitat_lvl==1 and upg:
        if resourceCheck(stronghold.t7_generator_lvl.cost[0][1], player):
            build(stronghold.t7_generator_lvl.cost[0][1], player)
            stronghold.t7_generator_lvl.habitat_lvl=2
            buy_building(stronghold.t7_generator_lvl.name, "stronghold")
            print('Behemoths upgraded!')
            return None
        else:
            print('Not enough resources!')

    # Freelancers Guild
    if not stronghold.freelancers_guild.built and stronghold.marketplace.built and builds:
        if resourceCheck(stronghold.freelancers_guild.cost[0], player):
            build(stronghold.freelancers_guild.cost[0], player)
            stronghold.freelancers_guild.built = True
            buy_building(stronghold.freelancers_guild.name, "stronghold")
            print('Freelancers Guild built!')
            return None
        else:
            print('Not enough resources!')

    # Resource Silo
    if not stronghold.resource_silo.built and stronghold.marketplace.built:
        if resourceCheck(stronghold.resource_silo.cost[0], player):
            build(stronghold.resource_silo.cost[0], player)
            stronghold.resource_silo.built = True
            player.daily_income[1] += 1
            player.daily_income[2] += 1
            buy_building(stronghold.resource_silo.name, "stronghold")
            print('Resource Silo built!')
            return None
        else:
            print('Not enough resources!')

    # Cyclops Cave
    if stronghold.t4_generator_lvl.habitat_lvl>=1 and stronghold.t6_generator_lvl.habitat_lvl==0 and hab:
        if resourceCheck(stronghold.t6_generator_lvl.cost[0][0], player):
            build(stronghold.t6_generator_lvl.cost[0][0], player)
            stronghold.t6_generator_lvl.habitat_lvl=1
            buy_building(stronghold.t6_generator_lvl.name, "stronghold")
            print('Cyclops Cave built!')
            return None
        else:
            print('Not enough resources!')

    # Upg. Cyclops Cave
    if stronghold.t6_generator_lvl.habitat_lvl==1 and upg:
        if resourceCheck(stronghold.t6_generator_lvl.cost[0][1], player):
            build(stronghold.t6_generator_lvl.cost[0][1], player)
            stronghold.t6_generator_lvl.habitat_lvl=2
            buy_building(stronghold.t6_generator_lvl.name, "stronghold")
            print('Upgraded Cyclops Cave!')
            return None
        else:
            print('Not enough resources!')

    # Mess Hall
    if stronghold.t1_generator_lvl.habitat_lvl>=1 and not stronghold.mess_hall.built and builds:
        if resourceCheck(stronghold.mess_hall.cost[0], player):
            build(stronghold.mess_hall.cost[0], player)
            stronghold.mess_hall.built = True
            buy_building(stronghold.mess_hall.name, "stronghold")
            print('Mess Hall built!')
            return None
        else:
            print('Not enough resources!')

    # Ballista Yard
    if not stronghold.ballists_yard.built and stronghold.blacksmith.built and builds:
        if resourceCheck(stronghold.ballists_yard.cost[0], player):
            build(stronghold.ballists_yard.cost[0], player)
            stronghold.ballists_yard.built = True
            buy_building(stronghold.ballists_yard.name, "stronghold")
            print('Ballista Yard built!')
            return None
        else:
            print('Not enough resources!')
