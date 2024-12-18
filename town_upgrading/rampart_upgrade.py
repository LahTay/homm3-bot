"""Script containing Rampart castle upgrade alghoritm"""
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


def rampartUpgrade(player, rampart):
    """
    Rampart castle upgrade alghoritm.
    :param player: Player object
    :param rampart: Rampart object
    :return: None
    """
    cost = full_unit_cost(rampart)
    if player.gold < (cost/3):
        print("Not enought gold for units, dont build anything")
        return None
    # ----------------------------HARDCODED ZONE-----------------------------------------------
    # 1 Tavern
    if rampart.tavern.built == False:
        if resourceCheck(rampart.tavern.cost[0], player):
            build(rampart.tavern.cost[0], player)
            rampart.tavern.built = True
            buy_building(rampart.tavern.name, "rampart")
            print('Tavern built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 2 Fort
    if rampart.tavern.built and rampart.fort.fort_lvl < 1:
        if resourceCheck(rampart.fort.cost[0][0], player):
            build(rampart.fort.cost[0][0], player)
            rampart.fort.fort_lvl = 1
            buy_building(rampart.fort.name, "rampart")
            print('Fort lvl 1 built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 3 Centaur Stables
    if rampart.fort.fort_lvl>=1 and rampart.t1_generator_lvl.habitat_lvl==0:
        if resourceCheck(rampart.t1_generator_lvl.cost[0][0], player):
            build(rampart.t1_generator_lvl.cost[0][0], player)
            rampart.t1_generator_lvl.habitat_lvl=1
            buy_building(rampart.t1_generator_lvl.name, "rampart")
            print('Centaur Stables built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 4 Homestead
    if rampart.t1_generator_lvl.habitat_lvl>=1 and rampart.t3_generator_lvl.habitat_lvl==0:
        if resourceCheck(rampart.t3_generator_lvl.cost[0][0], player):
            build(rampart.t3_generator_lvl.cost[0][0], player)
            rampart.t3_generator_lvl.habitat_lvl=1
            buy_building(rampart.t3_generator_lvl.name, "rampart")
            print('Homestead built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 5 Dwarf Cottage
    if rampart.t1_generator_lvl.habitat_lvl>=1 and rampart.t2_generator_lvl.habitat_lvl==0:
        if resourceCheck(rampart.t2_generator_lvl.cost[0][0], player):
            build(rampart.t2_generator_lvl.cost[0][0], player)
            rampart.t2_generator_lvl.habitat_lvl=1
            buy_building(rampart.t2_generator_lvl.name, "rampart")
            print('Dwarf Cottage built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 6 Town Hall
    if rampart.tavern.built and rampart.city_hall.city_hall_lvl <= 0:
        if resourceCheck(rampart.city_hall.cost[0][0], player):
            build(rampart.city_hall.cost[0][0], player)
            rampart.city_hall.city_hall_lvl = 1
            player.daily_income[0] += 500
            buy_building(rampart.city_hall.name, "rampart")
            print('Town Hall built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 7 Enchanted Spring
    if rampart.t3_generator_lvl.habitat_lvl>=1 and rampart.t4_generator_lvl.habitat_lvl==0:
        if resourceCheck(rampart.t4_generator_lvl.cost[0][0], player):
            build(rampart.t4_generator_lvl.cost[0][0], player)
            rampart.t4_generator_lvl.habitat_lvl=1
            buy_building(rampart.t4_generator_lvl.name, "rampart")
            print('Enchanted Spring built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 8 Mage Guild Level 1
    if rampart.fort.fort_lvl >= 1 and rampart.mage_guild.mage_guild_lvl < 1:
        if resourceCheck(rampart.mage_guild.cost[0][0], player):
            build(rampart.mage_guild.cost[0][0], player)
            rampart.mage_guild.mage_guild_lvl = 1
            buy_building(rampart.mage_guild.name, "rampart")
            print('Mage Guild Level 1 built')
            return None
        else:
            print('Not enough resources!')
            return None
            # ----------------------------HARDCODED ZONE-----------------------------------------------
    # [hab = build habitat], [upg = upgrade habitat], [wall = build/upgrade fort], [capi = build/upgrade city_hall], [MG_M = build Marketplace , upgrade/build mage_guild, build blacksmith], [builds = build other buildings]
    hab, upg, wall, capi, MG_M, builds = town_choice(player, rampart)

    # ------------------------------------------------------------------------------------------

    # 9 Marketplace
    if not rampart.marketplace.built and MG_M:
        if resourceCheck(rampart.marketplace.cost[0], player):
            build(rampart.marketplace.cost[0], player)
            rampart.marketplace.built = True
            buy_building(rampart.marketplace.name, "rampart")
            print('Marketplace built!')
            return None
        else:
            print('Not enough resources!')

    # 10 Blacksmith
    if not rampart.blacksmith.built and MG_M:
        if resourceCheck(rampart.blacksmith.cost[0], player):
            build(rampart.blacksmith.cost[0], player)
            rampart.blacksmith.built = True
            buy_building(rampart.blacksmith.name, "rampart")
            print('Blacksmith built!')
            return None
        else:
            print('Not enough resources!')

    # 11 City Hall
    if rampart.city_hall.city_hall_lvl == 1 and rampart.mage_guild.mage_guild_lvl >= 1 and rampart.blacksmith.built and rampart.marketplace.built and capi:
        if resourceCheck(rampart.city_hall.cost[0][1], player):
            build(rampart.city_hall.cost[0][1], player)
            rampart.city_hall.city_hall_lvl = 2
            player.daily_income[0] += 1000
            buy_building(rampart.city_hall.name, "rampart")
            print('City Hall built!')
            return None
        else:
            print('Not enough resources!')

    # 12 Capitol
    if rampart.city_hall.city_hall_lvl == 2 and rampart.fort.fort_lvl == 3 and capi:
        if resourceCheck(rampart.city_hall.cost[0][2], player):
            build(rampart.city_hall.cost[0][2], player)
            rampart.city_hall.city_hall_lvl = 3
            player.daily_income[0] += 2000
            buy_building(rampart.city_hall.name, "rampart")
            print('Capitol built!')
            return None
        else:
            print('Not enough resources!')

    # 13 Citadel
    if rampart.fort.fort_lvl == 1 and wall:
        if resourceCheck(rampart.fort.cost[0][1], player):
            build(rampart.fort.cost[0][1], player)
            rampart.fort.fort_lvl = 2
            buy_building(rampart.fort.name, "rampart")
            print('Citadel built!')
            return None
        else:
            print('Not enough resources!')

    # 14 Dendroid Arches
    if rampart.t3_generator_lvl.habitat_lvl>=1 and rampart.t5_generator_lvl.habitat_lvl==0 and builds:
        if resourceCheck(rampart.t5_generator_lvl.cost[0][0], player):
            build(rampart.t5_generator_lvl.cost[0][0], player)
            rampart.t5_generator_lvl.habitat_lvl=1
            buy_building(rampart.t5_generator_lvl.name, "rampart")
            print('Dendroid Arches built!')
            return None
        else:
            print('Not enough resources!')

    # 15 Upg. Homestead
    if rampart.t3_generator_lvl.habitat_lvl==1 and upg:
        if resourceCheck(rampart.t3_generator_lvl.cost[0][1], player):
            build(rampart.t3_generator_lvl.cost[0][1], player)
            rampart.t3_generator_lvl.habitat_lvl=2
            buy_building(rampart.t3_generator_lvl.name, "rampart")
            print('Homestead upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 16 Castle
    if rampart.fort.fort_lvl == 2 and wall:
        if resourceCheck(rampart.fort.cost[0][2], player):
            build(rampart.fort.cost[0][2], player)
            rampart.fort.fort_lvl = 3
            buy_building(rampart.fort.name, "rampart")
            print('Castle built!')
            return None
        else:
            print('Not enough resources!')

    # 17 Unicorn Glade
    if rampart.t4_generator_lvl.habitat_lvl>=1 and rampart.t6_generator_lvl.habitat_lvl==0 and rampart.t5_generator_lvl.habitat_lvl>=1 and hab:
        if resourceCheck(rampart.t6_generator_lvl.cost[0][0], player):
            build(rampart.t6_generator_lvl.cost[0][0], player)
            rampart.t6_generator_lvl.habitat_lvl=1
            buy_building(rampart.t6_generator_lvl.name, "rampart")
            print('Unicorn Glade built!')
            return None
        else:
            print('Not enough resources!')

    # 18 Mage Guild Level 2
    if rampart.mage_guild.mage_guild_lvl == 1 and MG_M:
        if resourceCheck(rampart.mage_guild.cost[0][1], player):
            build(rampart.mage_guild.cost[0][1], player)
            rampart.mage_guild.mage_guild_lvl = 2
            buy_building(rampart.mage_guild.name, "rampart")
            print('Mage Guild Level 2!')
            return None
        else:
            print('Not enough resources!')

    # 19 Mage Guild Level 3
    if rampart.mage_guild.mage_guild_lvl == 2 and MG_M:
        if resourceCheck(rampart.mage_guild.cost[0][2], player):
            build(rampart.mage_guild.cost[0][2], player)
            rampart.mage_guild.mage_guild_lvl = 3
            buy_building(rampart.mage_guild.name, "rampart")
            print('Mage Guild Level 3!')
            return None
        else:
            print('Not enough resources!')

    # 20 Miners Guild
    if rampart.t2_generator_lvl.habitat_lvl>=1 and rampart.miners_guild.built == False and builds:
        if resourceCheck(rampart.miners_guild.cost[0], player):
            build(rampart.miners_guild.cost[0], player)
            rampart.miners_guild.built = True
            buy_building(rampart.miners_guild.name, "rampart")
            print('Miners Guild built')
            return None
        else:
            print('Not enough resources!')

    # 21 Upg. Centaur Stables
    if rampart.t1_generator_lvl.habitat_lvl==1 and upg:
        if resourceCheck(rampart.t1_generator_lvl.cost[0][1], player):
            build(rampart.t1_generator_lvl.cost[0][1], player)
            rampart.t1_generator_lvl.habitat_lvl=2
            buy_building(rampart.t1_generator_lvl.name, "rampart")
            print('Centaur Stables upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 22 Upg. Dwarf Cottage
    if rampart.t2_generator_lvl.habitat_lvl==1 and upg:
        if resourceCheck(rampart.t2_generator_lvl.cost[0][1], player):
            build(rampart.t2_generator_lvl.cost[0][1], player)
            rampart.t2_generator_lvl.habitat_lvl=2
            buy_building(rampart.t2_generator_lvl.name, "rampart")
            print('Dwarf Cottage upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 23 Treasury
    if rampart.miners_guild.built and rampart.treasury.built == False and builds:
        if resourceCheck(rampart.treasury.cost[0], player):
            build(rampart.treasury.cost[0], player)
            rampart.treasury.built = True
            buy_building(rampart.treasury.name, "rampart")
            print('Treasury built')
            return None
        else:
            print('Not enough resources!')

    # 24 Dragon Cliffs
    if rampart.t6_generator_lvl.habitat_lvl>=1 and rampart.t7_generator_lvl.habitat_lvl==0 and rampart.mage_guild.mage_guild_lvl >= 2 and hab:
        if resourceCheck(rampart.t7_generator_lvl.cost[0][0], player):
            build(rampart.t7_generator_lvl.cost[0][0], player)
            rampart.t7_generator_lvl.habitat_lvl=1
            buy_building(rampart.t7_generator_lvl.name, "rampart")
            print('Dragon Cliffs built!')
            return None
        else:
            print('Not enough resources!')

    # 25 Upg. Unicorn Glade
    if rampart.t6_generator_lvl.habitat_lvl==1 and upg:
        if resourceCheck(rampart.t6_generator_lvl.cost[0][1], player):
            build(rampart.t6_generator_lvl.cost[0][1], player)
            rampart.t6_generator_lvl.habitat_lvl=2
            buy_building(rampart.t6_generator_lvl.name, "rampart")
            print('Unicorn Glade upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 26 Upg. Dragon Cliffs
    if rampart.t7_generator_lvl.habitat_lvl==1 and rampart.mage_guild.mage_guild_lvl >= 3 and upg:
        if resourceCheck(rampart.t7_generator_lvl.cost[0][1], player):
            build(rampart.t7_generator_lvl.cost[0][1], player)
            rampart.t7_generator_lvl.habitat_lvl=2
            buy_building(rampart.t7_generator_lvl.name, "rampart")
            print('Dragon Cliffs upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 27  Mage Guild Level 4
    if rampart.mage_guild.mage_guild_lvl == 3 and MG_M:
        if resourceCheck(rampart.mage_guild.cost[0][3], player):
            build(rampart.mage_guild.cost[0][3], player)
            rampart.mage_guild.mage_guild_lvl = 4
            buy_building(rampart.mage_guild.name, "rampart")
            print('Mage Guild Level 4!')
            return None
        else:
            print('Not enough resources!')

    # 28 Mage Guild Level 5
    if rampart.mage_guild.mage_guild_lvl == 4 and MG_M:
        if resourceCheck(rampart.mage_guild.cost[0][4], player):
            build(rampart.mage_guild.cost[0][4], player)
            rampart.mage_guild.mage_guild_lvl = 5
            buy_building(rampart.mage_guild.name, "rampart")
            print('Mage Guild Level 5!')
            return None
        else:
            print('Not enough resources!')

    if not rampart.resource_silo.built and rampart.marketplace.built:
        if resourceCheck(rampart.resource_silo.cost[0], player):
            build(rampart.resource_silo.cost[0], player)
            rampart.resource_silo.built = True
            player.daily_income[5] += 1
            buy_building(rampart.resource_silo.name, "rampart")
            print('Resource Silo built!')
            return None
        else:
            print('Not enough resources!')
