"""Script containing Inferno castle upgrade alghoritm"""
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


def infernoUpgrade(player, inferno):
    """
    Inferno castle upgrade alghoritm.
    :param player: player object
    :param inferno: Inferno object
    :return: None
    """
    cost = full_unit_cost(inferno)
    if player.gold < (cost/3):
        print("Not enought gold for units, dont build anything")
        return None
    # ----------------------------HARDCODED ZONE-----------------------------------------------
    # Tavern
    if not inferno.tavern.built:
        if resourceCheck(inferno.tavern.cost[0], player):
            build(inferno.tavern.cost[0], player)
            inferno.tavern.built = True
            buy_building(inferno.tavern.name, "inferno")
            print('Tavern built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # Fort
    if inferno.fort.fort_lvl == 0 and inferno.tavern.built:
        if resourceCheck(inferno.fort.cost[0][0], player):
            build(inferno.fort.cost[0][0], player)
            inferno.fort.built = True
            inferno.fort.fort_lvl = 1
            buy_building(inferno.fort.name, "inferno")
            print('Fort lvl 1 built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # Imp Crucible
    if inferno.t1_generator_lvl.habitat_lvl == 0 and inferno.fort.fort_lvl > 0:
        if resourceCheck(inferno.t1_generator_lvl.cost[0][0], player):
            build(inferno.t1_generator_lvl.cost[0][0], player)
            inferno.t1_generator_lvl.habitat_lvl = 1
            buy_building(inferno.t1_generator_lvl.name, "inferno")
            print('Imp crucible built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # Hall of Sins
    if inferno.t2_generator_lvl.habitat_lvl == 0 and inferno.t1_generator_lvl.built >= 1:
        if resourceCheck(inferno.t2_generator_lvl.cost[0][0], player):
            build(inferno.t2_generator_lvl.cost[0][0], player)
            inferno.t2_generator_lvl.habitat_lvl = 1
            buy_building(inferno.t2_generator_lvl.name, "inferno")
            print('Hall of sins built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # Town Hall
    if inferno.tavern.built and inferno.t2_generator_lvl.habitat_lvl >= 1 and inferno.city_hall.city_hall_lvl == 0:
        if resourceCheck(inferno.city_hall.cost[0][0], player):
            build(inferno.city_hall.cost[0][0], player)
            inferno.city_hall.city_hall_lvl = 1
            player.daily_income[0] += 500
            buy_building(inferno.city_hall.name, "inferno")
            print('Town Hall built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # Citadel
    if inferno.fort.fort_lvl == 1 and inferno.city_hall.city_hall_lvl >= 1:
        if resourceCheck(inferno.fort.cost[0][1], player):
            build(inferno.fort.cost[0][1], player)
            inferno.fort.fort_lvl = 2
            buy_building(inferno.fort.name, "inferno")
            print('Citadel built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # Kennels
    if inferno.t3_generator_lvl.habitat_lvl == 0 and inferno.fort.fort_lvl >= 2:
        if resourceCheck(inferno.t3_generator_lvl.cost[0][0], player):
            build(inferno.t3_generator_lvl.cost[0][0], player)
            inferno.t3_generator_lvl.habitat_lvl = 1
            buy_building(inferno.t3_generator_lvl.name, "inferno")
            print('Kennels built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # Mage Guild Level 1
    if inferno.mage_guild.mage_guild_lvl == 0 and inferno.t3_generator_lvl.habitat_lvl >= 1:
        if resourceCheck(inferno.mage_guild.cost[0][0], player):
            build(inferno.mage_guild.cost[0][0], player)
            inferno.mage_guild.mage_guild_lvl = 1
            buy_building(inferno.mage_guild.name, "inferno")
            print('Mage Guild Level 1 built!')
            return None
        else:
            print('Not enough resources!')
            return None
    # ----------------------------HARDCODED ZONE-----------------------------------------------
    # [hab = build habitat], [upg = upgrade habitat], [wall = build/upgrade fort], [capi = build/upgrade city_hall], [MG_M = build Marketplace , upgrade/build mage_guild, build blacksmith], [builds = build other buildings]
    hab, upg, wall, capi, MG_M, builds = town_choice(player, inferno)

    # ------------------------------------------------------------------------------------------
    # Blacksmith
    if not inferno.blacksmith.built and MG_M:
        if resourceCheck(inferno.blacksmith.cost[0], player):
            build(inferno.blacksmith.cost[0], player)
            inferno.blacksmith.built = True
            buy_building(inferno.blacksmith.name, "inferno")
            print('Blacksmith built!')
            return None
        else:
            print('Not enough resources!')

    # Marketplace
    if not inferno.marketplace.built and MG_M:
        if resourceCheck(inferno.marketplace.cost[0], player):
            build(inferno.marketplace.cost[0], player)
            inferno.marketplace.built = True
            buy_building(inferno.marketplace.name, "inferno")
            print('Marketplace built!')
            return None
        else:
            print('Not enough resources!')

    # City Hall
    if inferno.city_hall.city_hall_lvl == 1 and inferno.marketplace.built and inferno.blacksmith.built and inferno.mage_guild.mage_guild_lvl >= 1 and capi:
        if resourceCheck(inferno.city_hall.cost[0][1], player):
            build(inferno.city_hall.cost[0][1], player)
            inferno.city_hall.city_hall_lvl = 2
            player.daily_income[0] += 1000
            buy_building(inferno.city_hall.name, "inferno")
            print('City Hall built!')
            return None
        else:
            print('Not enough resources!')

    # Demon Gate
    if inferno.t4_generator_lvl.habitat_lvl == 0 and inferno.t2_generator_lvl.habitat_lvl >= 1 and hab:
        if resourceCheck(inferno.t4_generator_lvl.cost[0][0], player):
            build(inferno.t4_generator_lvl.cost[0][0], player)
            inferno.t4_generator_lvl.habitat_lvl = 1
            buy_building(inferno.t4_generator_lvl.name, "inferno")
            print('Demon Gate built!')
            return None
        else:
            print('Not enough resources!')

    # Hell Hole
    if inferno.t5_generator_lvl.habitat_lvl == 0 and inferno.t4_generator_lvl.habitat_lvl >= 1 and hab:
        if resourceCheck(inferno.t5_generator_lvl.cost[0][0], player):
            build(inferno.t5_generator_lvl.cost[0][0], player)
            inferno.t5_generator_lvl.habitat_lvl = 1
            buy_building(inferno.t5_generator_lvl.name, "inferno")
            print('Hell Hole built!')
            return None
        else:
            print('Not enough resources!')

    # Castle
    if inferno.fort.fort_lvl == 2 and wall:
        if resourceCheck(inferno.fort.cost[0][2], player):
            build(inferno.fort.cost[0][2], player)
            inferno.fort.fort_lvl = 3
            buy_building(inferno.fort.name, "inferno")
            print('Castle built!')
            return None
        else:
            print('Not enough resources!')

    # Capitol
    if inferno.fort.fort_lvl == 3 and inferno.city_hall.city_hall_lvl == 2 and capi:
        if resourceCheck(inferno.city_hall.cost[0][2], player):
            build(inferno.city_hall.cost[0][2], player)
            inferno.city_hall.city_hall_lvl = 3
            player.daily_income[0] += 2000
            buy_building(inferno.city_hall.name, "inferno")
            print('Capitol built!')
            return None
        else:
            print('Not enough resources!')

    # Upg. Imp crucible
    if inferno.t1_generator_lvl.habitat_lvl == 1 and upg:
        if resourceCheck(inferno.t1_generator_lvl.cost[0][1], player):
            build(inferno.t1_generator_lvl.cost[0][1], player)
            inferno.t1_generator_lvl.habitat_lvl = 2
            buy_building(inferno.t1_generator_lvl.name, "inferno")
            print('Imp crucible upgraded !')
            return None
        else:
            print('Not enough resources!')

    # Upg. Kennels
    if inferno.t3_generator_lvl.habitat_lvl == 1 and upg:
        if resourceCheck(inferno.t3_generator_lvl.cost[0][1], player):
            build(inferno.t3_generator_lvl.cost[0][1], player)
            inferno.t3_generator_lvl.habitat_lvl = 2
            buy_building(inferno.t3_generator_lvl.name, "inferno")
            print('Kennels upgraded!')
            return None
        else:
            print('Not enough resources!')

    # Upg. Hall of sins
    if inferno.t2_generator_lvl.habitat_lvl == 1 and upg:
        if resourceCheck(inferno.t2_generator_lvl.cost[0][1], player):
            build(inferno.t2_generator_lvl.cost[0][1], player)
            inferno.t2_generator_lvl.habitat_lvl = 2
            buy_building(inferno.t2_generator_lvl.name, "inferno")
            print('Hall of sins upgraded!')
            return None
        else:
            print('Not enough resources!')

    # Upg. Demon gate
    if inferno.t4_generator_lvl.habitat_lvl == 1 and upg:
        if resourceCheck(inferno.t4_generator_lvl.cost[0][1], player):
            build(inferno.t4_generator_lvl.cost[0][1], player)
            inferno.t4_generator_lvl.habitat_lvl = 2
            buy_building(inferno.t4_generator_lvl.name, "inferno")
            print('Demon gate upgraded!')
            return None
        else:
            print('Not enough resources!')

    # Mage guild Level 2
    if inferno.mage_guild.mage_guild_lvl == 1 and MG_M:
        if resourceCheck(inferno.mage_guild.cost[0][1], player):
            build(inferno.mage_guild.cost[0][1], player)
            inferno.mage_guild.mage_guild_lvl = 2
            buy_building(inferno.mage_guild.name, "inferno")
            print('Mage guild Level 2!')
            return None
        else:
            print('Not enough resources!')

    # Mage guild Level 3
    if inferno.mage_guild.mage_guild_lvl == 2 and MG_M:
        if resourceCheck(inferno.mage_guild.cost[0][2], player):
            build(inferno.mage_guild.cost[0][2], player)
            inferno.mage_guild.mage_guild_lvl = 3
            buy_building(inferno.mage_guild.name, "inferno")
            print('Mage guild Level 3!')
            return None
        else:
            print('Not enough resources!')

    # Fire Lake
    if inferno.mage_guild.mage_guild_lvl >= 1 and inferno.t4_generator_lvl.habitat_lvl >= 1 and inferno.t6_generator_lvl.habitat_lvl == 0 and hab:
        if resourceCheck(inferno.t6_generator_lvl.cost[0][0], player):
            build(inferno.t6_generator_lvl.cost[0][0], player)
            inferno.t6_generator_lvl.habitat_lvl = 1
            buy_building(inferno.t6_generator_lvl.name, "inferno")
            print('Fire Lake built!')
            return None
        else:
            print('Not enough resources!')

    # Forsaken Palace
    if inferno.t6_generator_lvl.habitat_lvl >= 1 and inferno.t7_generator_lvl.habitat_lvl == 0 and inferno.t5_generator_lvl.habitat_lvl >= 1 and hab:
        if resourceCheck(inferno.t7_generator_lvl.cost[0][0], player):
            build(inferno.t7_generator_lvl.cost[0][0], player)
            inferno.t7_generator_lvl.habitat_lvl = 1
            buy_building(inferno.t7_generator_lvl.name, "inferno")
            print('Forsaken Palace built!')
            return None
        else:
            print('Not enough resources!')

    # Mage guild Level 4
    if inferno.mage_guild.mage_guild_lvl == 3 and MG_M:
        if resourceCheck(inferno.mage_guild.cost[0][3], player):
            build(inferno.mage_guild.cost[0][3], player)
            inferno.mage_guild.mage_guild_lvl = 4
            buy_building(inferno.mage_guild.name, "inferno")
            print('Mage guild Level 4!')
            return None
        else:
            print('Not enough resources!')

    # Mage guild Level 5
    if inferno.mage_guild.mage_guild_lvl == 4 and MG_M:
        if resourceCheck(inferno.mage_guild.cost[0][4], player):
            build(inferno.mage_guild.cost[0][4], player)
            inferno.mage_guild.mage_guild_lvl = 5
            buy_building(inferno.mage_guild.name, "inferno")
            print('Mage guild Level 5 built!')
            return None
        else:
            print('Not enough resources!')

    # Upg. Hell Hole
    if inferno.mage_guild.mage_guild_lvl >= 2 and inferno.t5_generator_lvl.habitat_lvl == 1 and upg:
        if resourceCheck(inferno.t5_generator_lvl.cost[0][1], player):
            build(inferno.t5_generator_lvl.cost[0][1], player)
            inferno.t5_generator_lvl.habitat_lvl = 2
            buy_building(inferno.t5_generator_lvl.name, "inferno")
            print('Hell Hole upgraded!')
            return None
        else:
            print('Not enough resources!')

    # Upg. Forsaken Palace
    if inferno.t7_generator_lvl.habitat_lvl == 1 and upg:
        if resourceCheck(inferno.t7_generator_lvl.cost[0][1], player):
            build(inferno.t7_generator_lvl.cost[0][1], player)
            inferno.t7_generator_lvl.habitat_lvl = 2
            buy_building(inferno.t7_generator_lvl.name, "inferno")
            print('Forsaken Palace upgraded!')
            return None
        else:
            print('Not enough resources!')

    # Upg. Fire Lake
    if inferno.t6_generator_lvl.habitat_lvl == 1 and upg:
        if resourceCheck(inferno.t6_generator_lvl.cost[0][1], player):
            build(inferno.t6_generator_lvl.cost[0][1], player)
            inferno.t6_generator_lvl.habitat_lvl = 2
            buy_building(inferno.t6_generator_lvl.name, "inferno")
            print('Fire Lake upgraded!')
            return None
        else:
            print('Not enough resources!')

    # Order of Fire
    if inferno.mage_guild.mage_guild_lvl >= 1 and inferno.order_of_fire.built == False and builds:
        if resourceCheck(inferno.order_of_fire.cost[0], player):
            build(inferno.order_of_fire.cost[0], player)
            inferno.order_of_fire.built = True
            buy_building(inferno.order_of_fire.name, "inferno")
            print('Order of Fire built!')
            return None
        else:
            print('Not enough resources!')

    # Cages
    if inferno.t3_generator_lvl.habitat_lvl >= 1 and inferno.cages.built == False and builds:
        if resourceCheck(inferno.cages.cost[0], player):
            build(inferno.cages.cost[0], player)
            inferno.cages.built = True
            buy_building(inferno.cages.name, "inferno")
            print('Cages built!')
            return None
        else:
            print('Not enough resources!')

    # Birthing Pools
    if inferno.t1_generator_lvl.habitat_lvl >= 1 and inferno.birthing_pools.built == False and builds:
        if resourceCheck(inferno.birthing_pools.cost[0], player):
            build(inferno.birthing_pools.cost[0], player)
            inferno.birthing_pools.built = True
            buy_building(inferno.birthing_pools.name, "inferno")
            print('Birthing Pool built!')
            return None
        else:
            print('Not enough resources!')

    # Castle Gate
    if inferno.fort.fort_lvl >= 2 and inferno.castle_gate.built == False and builds:
        if resourceCheck(inferno.castle_gate.cost[0], player):
            build(inferno.castle_gate.cost[0], player)
            inferno.castle_gate.built = True
            buy_building(inferno.castle_gate.name, "inferno")
            print('Castle Gate built!')
            return None
        else:
            print('Not enough resources!')

    # Brimstone Stormclouds
    if inferno.fort.fort_lvl >= 1 and inferno.brimstone_stormclouds.built == False and builds:
        if resourceCheck(inferno.brimstone_stormclouds.cost[0], player):
            build(inferno.brimstone_stormclouds.cost[0], player)
            inferno.brimstone_stormclouds.built = True
            buy_building(inferno.brimstone_stormclouds.name, "inferno")
            print('Brimstone Stormclouds built!')
            return None
        else:
            print('Not enough resources!')

    # Resource Silo
    if inferno.resource_silo.built == False and inferno.marketplace.built:
        if resourceCheck(inferno.resource_silo.cost[0], player):
            build(inferno.resource_silo.cost[0], player)
            inferno.resource_silo.built = True
            player.daily_income[3] += 1
            buy_building(inferno.resource_silo.name, "inferno")
            print('Resource Silo built!')
            return None
        else:
            print('Not enough resources!')
