"""Script containing Fortress castle upgrade alghoritm"""
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


def fortressUpgrade(player, fortress):
    """
    Fortress castle upgrade alghoritm.
    :param player: player object
    :param fortress: conflux object
    :return: None
    """
    cost = full_unit_cost(fortress)
    if player.gold < (cost/3):
        print("Not enought gold for units, dont build anything")
        return None
    # ----------------------------HARDCODED ZONE-----------------------------------------------
    # 1 Tavern
    if not fortress.tavern.built:
        if resourceCheck(fortress.tavern.cost[0], player):
            build(fortress.tavern.cost[0], player)
            fortress.tavern.built = True
            buy_building(fortress.tavern.name, "fortress")
            print('Tavern built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 2 Fort
    if fortress.tavern.built and fortress.fort.fort_lvl < 1:
        if resourceCheck(fortress.fort.cost[0][0], player):
            build(fortress.fort.cost[0][0], player)
            fortress.fort.fort_lvl = 1
            buy_building(fortress.fort.name, "fortress")
            print('Fort lvl 1 built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 3 Gnoll Hut
    if fortress.fort.fort_lvl>=1 and fortress.t1_generator_lvl.habitat_lvl==0:
        if resourceCheck(fortress.t1_generator_lvl.cost[0][0], player):
            build(fortress.t1_generator_lvl.cost[0][0], player)
            fortress.t1_generator_lvl.habitat_lvl=1
            buy_building(fortress.t1_generator_lvl.name, "fortress")
            print('Gnoll Hut built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 4 Lizard Den
    if fortress.t2_generator_lvl.habitat_lvl == 0 and fortress.t1_generator_lvl.habitat_lvl >= 1:
        if resourceCheck(fortress.t2_generator_lvl.cost[0][0], player):
            build(fortress.t2_generator_lvl.cost[0][0], player)
            fortress.t2_generator_lvl.habitat_lvl = 1
            buy_building(fortress.t2_generator_lvl.name, "fortress")
            print('Lizard Den built!')
            return None
        else:
            print('Not enough resources!')
            return None


    # 4.5 Wyvern Nest
    print(fortress.t6_generator_lvl.habitat_lvl)
    if fortress.t6_generator_lvl.habitat_lvl == 0 and fortress.t2_generator_lvl.habitat_lvl >= 1:
        if resourceCheck(fortress.t6_generator_lvl.cost[0][0], player):
            build(fortress.t6_generator_lvl.cost[0][0], player)
            fortress.t6_generator_lvl.habitat_lvl = 1
            buy_building(fortress.t6_generator_lvl.name, "fortress")
            print('Wyvern Nest built!')
            return None
        else:
            print('Not enough resources!')
            return None


    # 5 Serpent Fly Hive
    if fortress.t3_generator_lvl.habitat_lvl == 0 and fortress.t2_generator_lvl.habitat_lvl >= 1:
        if resourceCheck(fortress.t3_generator_lvl.cost[0][0], player):
            build(fortress.t3_generator_lvl.cost[0][0], player)
            fortress.t3_generator_lvl.habitat_lvl = 1
            buy_building(fortress.t3_generator_lvl.name, "fortress")
            print('Serpent Fly Hive built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 6 Town Hall
    if fortress.tavern.built and fortress.city_hall.city_hall_lvl <= 0:
        if resourceCheck(fortress.city_hall.cost[0][0], player):
            build(fortress.city_hall.cost[0][0], player)
            fortress.city_hall.city_hall_lvl = 1
            player.daily_income[0] += 500
            buy_building(fortress.city_hall.name, "fortress")
            print('Town Hall built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 7 Citadel
    if fortress.fort.fort_lvl == 1 and fortress.city_hall.city_hall_lvl == 1:
        if resourceCheck(fortress.fort.cost[0][1], player):
            build(fortress.fort.cost[0][1], player)
            fortress.fort.fort_lvl = 2
            buy_building(fortress.fort.name, "fortress")
            print('Citadel built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 8 Basilisk Pit
    if fortress.t4_generator_lvl.habitat_lvl==0 and fortress.fort.fort_lvl >= 2:
        if resourceCheck(fortress.t4_generator_lvl.cost[0][0], player):
            build(fortress.t4_generator_lvl.cost[0][0], player)
            fortress.t4_generator_lvl.habitat_lvl=1
            buy_building(fortress.t4_generator_lvl.name, "fortress")
            print('Basilisk Pit built!')
            return None
        else:
            print('Not enough resources!')
            return None
    # ----------------------------HARDCODED ZONE-----------------------------------------------
    # [hab = build habitat], [upg = upgrade habitat], [wall = build/upgrade fort], [capi = build/upgrade city_hall], [MG_M = build Marketplace , upgrade/build mage_guild, build blacksmith], [builds = build other buildings]
    hab, upg, wall, capi, MG_M, builds = town_choice(player, fortress)

    # ------------------------------------------------------------------------------------------
    # 9 Upg. Lizard Den
    if fortress.t2_generator_lvl.habitat_lvl==1 and upg:
        if resourceCheck(fortress.t2_generator_lvl.cost[0][1], player):
            build(fortress.t2_generator_lvl.cost[0][1], player)
            fortress.t2_generator_lvl.habitat_lvl=2
            buy_building(fortress.t2_generator_lvl.name, "fortress")
            print('Lizard Den upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 10 Mage Guild Level 1
    if fortress.mage_guild.mage_guild_lvl == 0 and MG_M:
        if resourceCheck(fortress.mage_guild.cost[0][0], player):
            build(fortress.mage_guild.cost[0][0], player)
            fortress.mage_guild.mage_guild_lvl = 1
            buy_building(fortress.mage_guild.name, "fortress")
            print('Mage Guild Level 1!')
            return None
        else:
            print('Not enough resources!')

    # 11 Marketplace
    if not fortress.marketplace.built and MG_M:
        if resourceCheck(fortress.marketplace.cost[0], player):
            build(fortress.marketplace.cost[0], player)
            fortress.marketplace.built = True
            buy_building(fortress.marketplace.name, "fortress")
            print('Marketplace built!')
            return None
        else:
            print('Not enough resources!')

    # 12 Blacksmith
    if not fortress.blacksmith.built and MG_M:
        if resourceCheck(fortress.blacksmith.cost[0], player):
            build(fortress.blacksmith.cost[0], player)
            fortress.blacksmith.built = True
            buy_building(fortress.blacksmith.name, "fortress")
            print('Blacksmith built!')
            return None
        else:
            print('Not enough resources!')

    # 13 City Hall
    if fortress.city_hall.city_hall_lvl == 0 and fortress.blacksmith.built and fortress.mage_guild.mage_guild_lvl >= 1 and fortress.marketplace.built and capi:
        if resourceCheck(fortress.city_hall.cost[0][1], player):
            build(fortress.city_hall.cost[0][1], player)
            fortress.city_hall.city_hall_lvl = 2
            player.daily_income[0] += 1000
            buy_building(fortress.city_hall.name, "fortress")
            print('City Hall built!')
            return None
        else:
            print('Not enough resources!')

    # 14 Upg. Gnoll Hut
    if fortress.t1_generator_lvl.habitat_lvl==1 and fortress.city_hall.city_hall_lvl >= 1 and upg:
        if resourceCheck(fortress.t1_generator_lvl.cost[0][1], player):
            build(fortress.t1_generator_lvl.cost[0][1], player)
            fortress.t1_generator_lvl.habitat_lvl=2
            buy_building(fortress.t1_generator_lvl.name, "fortress")
            print('Gnoll Hut upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 15 Upg. Serpent Fly Hive
    if fortress.t3_generator_lvl.habitat_lvl==1 and upg:
        if resourceCheck(fortress.t3_generator_lvl.cost[0][1], player):
            build(fortress.t3_generator_lvl.cost[0][1], player)
            fortress.t3_generator_lvl.upgraded = True
            buy_building(fortress.t3_generator_lvl.name, "fortress")
            print('Serpent Fly Hive upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 16 Castle
    if fortress.fort.fort_lvl == 2 and wall:
        if resourceCheck(fortress.fort.cost[0][2], player):
            build(fortress.fort.cost[0][2], player)
            fortress.fort.fort_lvl = 3
            buy_building(fortress.fort.name, "fortress")
            print('Castle built!')
            return None
        else:
            print('Not enough resources!')

    # 17 Capitol
    if fortress.city_hall.city_hall_lvl == 2 and fortress.fort.fort_lvl == 3 and capi:
        if resourceCheck(fortress.city_hall.cost[0][2], player):
            build(fortress.city_hall.cost[0][2], player)
            fortress.city_hall.city_hall_lvl = 3
            player.daily_income[0] += 2000
            buy_building(fortress.city_hall.name, "fortress")
            print('Capitol built!')
            return None
        else:
            print('Not enough resources!')

    # 18 Basilisk Pit
    if fortress.t4_generator_lvl.habitat_lvl==0 and fortress.t3_generator_lvl.habitat_lvl>=1 and hab:
        if resourceCheck(fortress.t4_generator_lvl.cost[0][0], player):
            build(fortress.t4_generator_lvl.cost[0][0], player)
            fortress.t4_generator_lvl.habitat_lvl=1
            buy_building(fortress.t4_generator_lvl.name, "fortress")
            print('Basilisk Pit built!')
            return None
        else:
            print('Not enough resources!')

    # 19 Gorgon Lair
    if fortress.t5_generator_lvl.habitat_lvl==0 and fortress.t3_generator_lvl.habitat_lvl>=1 and fortress.t2_generator_lvl.habitat_lvl>=1 and hab:
        if resourceCheck(fortress.t5_generator_lvl.cost[0][0], player):
            build(fortress.t5_generator_lvl.cost[0][0], player)
            fortress.t5_generator_lvl.habitat_lvl=1
            buy_building(fortress.t5_generator_lvl.name, "fortress")
            print('Gorgon Lair built!')
            return None
        else:
            print('Not enough resources!')

    # 20 Glyphs of Fear
    if not fortress.glyphs_of_fear.built and fortress.fort.fort_lvl>=1 and builds:
        if resourceCheck(fortress.glyphs_of_fear.cost[0], player):
            build(fortress.glyphs_of_fear.cost[0], player)
            fortress.glyphs_of_fear.built = True
            buy_building(fortress.glyphs_of_fear.name, "fortress")
            print("Glyphs of Fear built!")
            return None
        else:
            print('Not enough resources!')

    # 21 Cage of Warlords
    if not fortress.cage_of_warlords.built and fortress.glyphs_of_fear.built and fortress.city_hall.city_hall_lvl >= 1 and builds:
        if resourceCheck(fortress.cage_of_warlords.cost[0], player):
            build(fortress.cage_of_warlords.cost[0], player)
            fortress.cage_of_warlords.built = True
            buy_building(fortress.cage_of_warlords.name, "fortress")
            print("Cage of Warlords")
            return None
        else:
            print('Not enough resources!')

    # 22 Mage Guild Level 2
    if fortress.mage_guild.mage_guild_lvl == 1 and MG_M:
        if resourceCheck(fortress.mage_guild.cost[0][1], player):
            build(fortress.mage_guild.cost[0][1], player)
            fortress.mage_guild.mage_guild_lvl = 2
            buy_building(fortress.mage_guild.name, "fortress")
            print('Mage Guild Level 2!')
            return None
        else:
            print('Not enough resources!')

    # 23 Mage Guild Level 3
    if fortress.mage_guild.mage_guild_lvl == 2 and MG_M:
        if resourceCheck(fortress.mage_guild.cost[0][2], player):
            build(fortress.mage_guild.cost[0][2], player)
            fortress.mage_guild.mage_guild_lvl = 3
            buy_building(fortress.mage_guild.name, "fortress")
            print('Mage Guild Level 3!')
            return None
        else:
            print('Not enough resources!')

    # 24 Upg. Gorgon Lair
    if fortress.t5_generator_lvl.habitat_lvl==1 and fortress.resource_silo.built and upg:
        if resourceCheck(fortress.t5_generator_lvl.cost[0][1], player):
            build(fortress.t5_generator_lvl.cost[0][1], player)
            fortress.t5_generator_lvl.upgraded = True
            buy_building(fortress.t5_generator_lvl.name, "fortress")
            print('Gorgon Lair upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 25 Captains Quarters
    if not fortress.captains_quarters.built and fortress.t1_generator_lvl.habitat_lvl>=1 and builds:
        if resourceCheck(fortress.captains_quarters.cost[0], player):
            build(fortress.captains_quarters.cost[0], player)
            fortress.captains_quarters.built = True
            buy_building(fortress.captains_quarters.name, "fortress")
            print("Captains Quarters built")
            return None
        else:
            print('Not enough resources!')

    # 26 Upg. Basilisk Pit
    if not fortress.t4_generator_lvl.habitat_lvl==1 and upg:
        if resourceCheck(fortress.t4_generator_lvl.cost[0][1], player):
            build(fortress.t4_generator_lvl.cost[0][1], player)
            fortress.t4_generator_lvl.habitat_lvl=2
            buy_building(fortress.t4_generator_lvl.name, "fortress")
            print('Basilisk Pit Upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 27 Resource Silo
    if not fortress.resource_silo.built and fortress.marketplace.built:
        if resourceCheck(fortress.resource_silo.cost[0], player):
            build(fortress.resource_silo.cost[0], player)
            fortress.resource_silo.built = True
            player.daily_income[1] += 1
            player.daily_income[2] += 1
            buy_building(fortress.resource_silo.name, "fortress")
            print('Resource Silo built!')
            return None
        else:
            print('Not enough resources!')

    # 28 Hydra Pond
    if fortress.t7_generator_lvl.habitat_lvl==0 and fortress.t6_generator_lvl.habitat_lvl>=1 and fortress.t4_generator_lvl.habitat_lvl>=1 and hab:
        if resourceCheck(fortress.t7_generator_lvl.cost[0][0], player):
            build(fortress.t7_generator_lvl.cost[0][0], player)
            fortress.t7_generator_lvl.habitat_lvl=1
            buy_building(fortress.t7_generator_lvl.name, "fortress")
            print('Hydra Pond built!')
            return None
        else:
            print('Not enough resources!')


    # 29 Upg. Wyvern Nest
    if fortress.t6_generator_lvl.habitat_lvl==1 and upg:
        if resourceCheck(fortress.t6_generator_lvl.cost[0][1], player):
            build(fortress.t6_generator_lvl.cost[0][1], player)
            fortress.t6_generator_lvl.habitat_lvl=2
            buy_building(fortress.t6_generator_lvl.name, "fortress")
            print('Wyvern Nest upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 30 Upg. Hydra Pond
    if fortress.t7_generator_lvl.habitat_lvl==1 and upg:
        if resourceCheck(fortress.t7_generator_lvl.cost[0][1], player):
            build(fortress.t7_generator_lvl.cost[0][1], player)
            fortress.t7_generator_lvl.habitat_lvl=2
            buy_building(fortress.t7_generator_lvl.name, "fortress")
            print('Hydra Pond Upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 31 Blood Obelisk
    if not fortress.blood_obelisk.built and fortress.glyphs_of_fear.built and builds:
        if resourceCheck(fortress.blood_obelisk.cost[0], player):
            build(fortress.blood_obelisk.cost[0], player)
            fortress.blood_obelisk.built = True
            buy_building(fortress.blood_obelisk.name, "fortress")
            print("Blood Obelisk built!")
            return None
        else:
            print('Not enough resources!')
