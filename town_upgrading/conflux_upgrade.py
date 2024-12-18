"""Script containing Conflux castle upgrade alghoritm"""
from town_upgrading.choice_generator import town_choice,full_unit_cost
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


def confluxUpgrade(player, conflux):
    """
    Conflux castle upgrade alghoritm.
    :param player: Player object
    :param conflux: Conflux object
    :return: None
    """
    cost = full_unit_cost(conflux)
    if player.gold < (cost/3):
        print("Not enought gold for units, dont build anything")
        return None
    # ----------------------------HARDCODED ZONE-----------------------------------------------
    # 1 Tavern
    if not conflux.tavern.built:
        if resourceCheck(conflux.tavern.cost[0], player):
            build(conflux.tavern.cost[0], player)
            conflux.tavern.built = True
            buy_building(conflux.tavern.name, "conflux")
            print('Tavern built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 2 Fort                            <our rule>
    if conflux.fort.fort_lvl == 0 and conflux.tavern.built:
        if resourceCheck(conflux.fort.cost[0][0], player):
            build(conflux.fort.cost[0][0], player)
            conflux.fort.fort_lvl = 1
            buy_building(conflux.fort.name, "conflux")
            print('Fort lvl 1 built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 3 Magic Lantern
    if conflux.t1_generator_lvl.habitat_lvl == 0 and conflux.fort.fort_lvl >= 1:
        if resourceCheck(conflux.t1_generator_lvl.cost[0][0], player):
            build(conflux.t1_generator_lvl.cost[0][0], player)
            conflux.t1_generator_lvl.habitat_lvl = 1
            buy_building(conflux.t1_generator_lvl.name, "conflux")
            print('Magic Lantern built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 4 Mage Guild Level 1                       <our rule>
    if conflux.mage_guild.mage_guild_lvl == 0 and conflux.t1_generator_lvl.habitat_lvl >= 1:
        if resourceCheck(conflux.mage_guild.cost[0][0], player):
            build(conflux.mage_guild.cost[0][0], player)
            conflux.mage_guild.mage_guild_lvl = 1
            buy_building(conflux.mage_guild.name, "conflux")
            print('Mage Guild Level 1!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 5 Altar of Air
    if conflux.t2_generator_lvl.habitat_lvl == 0 and conflux.mage_guild.mage_guild_lvl >= 1 and conflux.t1_generator_lvl.habitat_lvl >= 1:
        if resourceCheck(conflux.t2_generator_lvl.cost[0][0], player):
            build(conflux.t2_generator_lvl.cost[0][0], player)
            conflux.t2_generator_lvl.habitat_lvl = 1
            buy_building(conflux.t2_generator_lvl.name, "conflux")
            print('Altair of Air built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 6 Altar of Water
    if conflux.t3_generator_lvl.habitat_lvl == 0 and conflux.mage_guild.mage_guild_lvl >= 1 and conflux.t1_generator_lvl.habitat_lvl >= 1:
        if resourceCheck(conflux.t3_generator_lvl.cost[0][0], player):
            build(conflux.t3_generator_lvl.cost[0][0], player)
            conflux.t3_generator_lvl.habitat_lvl = 1
            buy_building(conflux.t3_generator_lvl.name, "conflux")
            print('Altar of Water built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 7 Town Hall                                      <our rule>
    if conflux.city_hall.city_hall_lvl == 0 and conflux.mage_guild.mage_guild_lvl >= 1 and conflux.tavern.built:
        if resourceCheck(conflux.city_hall.cost[0][0], player):
            build(conflux.city_hall.cost[0][0], player)
            conflux.city_hall.city_hall_lvl = 1
            buy_building(conflux.city_hall.name, "conflux")
            print('Town Hall built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 8 Citadel                             <our rule>
    if conflux.fort.fort_lvl == 1 and conflux.city_hall.city_hall_lvl >= 1:
        if resourceCheck(conflux.fort.cost[0][1], player):
            build(conflux.fort.cost[0][1], player)
            conflux.fort.fort_lvl = 2
            buy_building(conflux.fort.name, "conflux")
            print('Citadel built!')
            return None
        else:
            print('Not enough resources!')
            return None
    # ----------------------------HARDCODED ZONE-----------------------------------------------
    # [hab = build habitat], [upg = upgrade habitat], [wall = build/upgrade fort], [capi = build/upgrade city_hall], [MG_M = build Marketplace , upgrade/build mage_guild, build blacksmith], [builds = build other buildings]
    hab, upg, wall, capi, MG_M, builds = town_choice(player, conflux)

    # ------------------------------------------------------------------------------------------
    # 9 Altar of Fire
    if conflux.t4_generator_lvl.habitat_lvl == 0 and conflux.t2_generator_lvl.habitat_lvl >= 1 and hab:
        if resourceCheck(conflux.t4_generator_lvl.cost[0][0], player):
            build(conflux.t4_generator_lvl.cost[0][0], player)
            conflux.t4_generator_lvl.habitat_lvl = 1
            buy_building(conflux.t4_generator_lvl.name, "conflux")
            print('Altar of Fire built!')
            return None
        else:
            print('Not enough resources!')

    # 10 Marketplace
    if not conflux.marketplace.built and MG_M:
        if resourceCheck(conflux.marketplace.cost[0], player):
            build(conflux.marketplace.cost[0], player)
            conflux.marketplace.built = True
            buy_building(conflux.marketplace.name, "conflux")
            print('Marketplace built!')
            return None
        else:
            print('Not enough resources!')

    # 11 Blacksmith
    if not conflux.blacksmith.built and MG_M:
        if resourceCheck(conflux.blacksmith.cost[0], player):
            build(conflux.blacksmith.cost[0], player)
            conflux.blacksmith.built = True
            buy_building(conflux.blacksmith.name, "conflux")
            print('Blacksmith built!')
            return None
        else:
            print('Not enough resources!')

    # 12 City Hall
    if conflux.city_hall.city_hall_lvl == 1 and conflux.blacksmith.built and conflux.mage_guild.mage_guild_lvl >= 1 and conflux.marketplace.built and capi:
        if resourceCheck(conflux.city_hall.cost[0][1], player):
            build(conflux.city_hall.cost[0][1], player)
            conflux.city_hall.city_hall_lvl = 2
            buy_building(conflux.city_hall.name, "conflux")
            print('City Hall built!')
            return None
        else:
            print('Not enough resources!')

    # 13 Upg. Altar of Water
    if conflux.t3_generator_lvl.habitat_lvl == 1 and upg:
        if resourceCheck(conflux.t3_generator_lvl.cost[0][1], player):
            build(conflux.t3_generator_lvl.cost[0][1], player)
            conflux.t3_generator_lvl.habitat_lvl = 2
            buy_building(conflux.t3_generator_lvl.name, "conflux")
            print('Altar of Water upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 14 Garden of Life
    if not conflux.garden_of_life.built and conflux.t1_generator_lvl.habitat_lvl >= 1 and builds:
        if resourceCheck(conflux.garden_of_life.cost[0], player):
            build(conflux.garden_of_life.cost[0], player)
            conflux.garden_of_life.built = True
            buy_building(conflux.garden_of_life.name, "conflux")
            print("Garden of Life built!")
            return None
        else:
            print('Not enough resources!')

    # 15 Mage Guild Level 2
    if conflux.mage_guild.mage_guild_lvl == 1 and MG_M:
        if resourceCheck(conflux.mage_guild.cost[0][1], player):
            build(conflux.mage_guild.cost[0][1], player)
            conflux.mage_guild.mage_guild_lvl = 2
            buy_building(conflux.mage_guild.name, "conflux")
            print('Mage Guild Level 2!')
            return None
        else:
            print('Not enough resources!')

    # 16 Castle
    if conflux.fort.fort_lvl == 2 and wall:
        if resourceCheck(conflux.fort.cost[0][2], player):
            build(conflux.fort.cost[0][2], player)
            conflux.fort.fort_lvl = 3
            buy_building(conflux.fort.name, "conflux")
            print('Castle built!')
            return None
        else:
            print('Not enough resources!')

    # 17 Capitol
    if conflux.fort.fort_lvl >= 3 and conflux.city_hall.city_hall_lvl == 2 and capi:
        if resourceCheck(conflux.city_hall.cost[0][2], player):
            build(conflux.city_hall.cost[0][2], player)
            conflux.city_hall.city_hall_lvl = 3
            buy_building(conflux.city_hall.name, "conflux")
            print('Capitol built!')
            return None
        else:
            print('Not enough resources!')

    # 18 Altar of Earth
    if conflux.t5_generator_lvl.habitat_lvl == 0 and conflux.t3_generator_lvl.habitat_lvl >= 1 and hab:
        if resourceCheck(conflux.t5_generator_lvl.cost[0][0], player):
            build(conflux.t5_generator_lvl.cost[0][0], player)
            conflux.t5_generator_lvl.habitat_lvl = 1
            buy_building(conflux.t5_generator_lvl.name, "conflux")
            print('Altar of Earth built!')
            return None
        else:
            print('Not enough resources!')

    # 19 Upg. Altar of Air
    if conflux.t2_generator_lvl.habitat_lvl == 1 and upg:
        if resourceCheck(conflux.t2_generator_lvl.cost[0][1], player):
            build(conflux.t2_generator_lvl.cost[0][1], player)
            conflux.t2_generator_lvl.habitat_lvl = 2
            buy_building(conflux.t2_generator_lvl.name, "conflux")
            print('Altar of Air upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 20 Upg. Magic Lantern
    if conflux.t1_generator_lvl.habitat_lvl == 1 and conflux.magic_university.built and upg:
        if resourceCheck(conflux.t1_generator_lvl.cost[0][1], player):
            build(conflux.t1_generator_lvl.cost[0][1], player)
            conflux.t1_generator_lvl.habitat_lvl = 2
            buy_building(conflux.t1_generator_lvl.name, "conflux")
            print('Magic Lantern upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 21 Upg. Altar of Fire
    if conflux.t4_generator_lvl.habitat_lvl == 1 and upg:
        if resourceCheck(conflux.t4_generator_lvl.cost[0][1], player):
            build(conflux.t4_generator_lvl.cost[0][1], player)
            conflux.t4_generator_lvl.habitat_lvl = 2
            buy_building(conflux.t4_generator_lvl.name, "conflux")
            print('Altar of Fire Upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 22 Mage Guild Level 3
    if conflux.mage_guild.mage_guild_lvl == 2 and MG_M:
        if resourceCheck(conflux.mage_guild.cost[0][2], player):
            build(conflux.mage_guild.cost[0][2], player)
            conflux.mage_guild.mage_guild_lvl = 3
            buy_building(conflux.mage_guild.name, "conflux")
            print('Mage Guild Level 3!')
            return None
        else:
            print('Not enough resources!')

    # 23 Altar of Thought
    if conflux.t6_generator_lvl.habitat_lvl == 0 and conflux.t5_generator_lvl.habitat_lvl >= 1 and hab:
        if resourceCheck(conflux.t6_generator_lvl.cost[0][0], player):
            build(conflux.t6_generator_lvl.cost[0][0], player)
            conflux.t6_generator_lvl.habitat_lvl = 1
            buy_building(conflux.t6_generator_lvl.name, "conflux")
            print('Altar of Thought built!')
            return None
        else:
            print('Not enough resources!')

    # 24 Magic University
    if not conflux.magic_university.built and conflux.mage_guild.mage_guild_lvl >= 1 and builds:
        if resourceCheck(conflux.magic_university.cost[0], player):
            build(conflux.magic_university.cost[0], player)
            conflux.magic_university.built = True
            buy_building(conflux.magic_university.name, "conflux")
            print("Magic University built!")
            return None
        else:
            print('Not enough resources!')

    # 25 Upg. Altar of Earth
    if conflux.t5_generator_lvl.habitat_lvl == 1 and upg:
        if resourceCheck(conflux.t5_generator_lvl.cost[0][1], player):
            build(conflux.t5_generator_lvl.cost[0][1], player)
            conflux.t5_generator_lvl.habitat_lvl = 2
            buy_building(conflux.t5_generator_lvl.name, "conflux")
            print('CAltar of Earth upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 26 Resource Silo
    if not conflux.resource_silo.built and conflux.marketplace.built:
        if resourceCheck(conflux.resource_silo.cost[0], player):
            build(conflux.resource_silo.cost[0], player)
            conflux.resource_silo.built = True
            buy_building(conflux.resource_silo.name, "conflux")
            print('Resource Silo built!')
            return None
        else:
            print('Not enough resources!')

    # 27 Pyre
    if conflux.t7_generator_lvl.habitat_lvl == 0 and conflux.t6_generator_lvl.habitat_lvl >= 1 and hab:
        if resourceCheck(conflux.t7_generator_lvl.cost[0][0], player):
            build(conflux.t7_generator_lvl.cost[0][0], player)
            conflux.t7_generator_lvl.habitat_lvl = 1
            buy_building(conflux.t7_generator_lvl.name, "conflux")
            print('Pyre built!')
            return None
        else:
            print('Not enough resources!')

    # 28 Mage Guild Level 4
    if conflux.mage_guild.mage_guild_lvl == 3 and MG_M:
        if resourceCheck(conflux.mage_guild.cost[0][3], player):
            build(conflux.mage_guild.cost[0][3], player)
            conflux.mage_guild.mage_guild_lvl = 4
            buy_building(conflux.mage_guild.name, "conflux")
            print("Mage Guild Level 4!")
            return None
        else:
            print('Not enough resources!')

    # 29 Mage Guild Level 5
    if conflux.mage_guild.mage_guild_lvl == 4 and MG_M:
        if resourceCheck(conflux.mage_guild.cost[0][4], player):
            build(conflux.mage_guild.cost[0][4], player)
            conflux.mage_guild.mage_guild_lvl = 5
            buy_building(conflux.mage_guild.name, "conflux")
            print("Mage Guild Level 5!")
            return None
        else:
            print('Not enough resources!')

    # 30 Upg. Altar of Thought
    if conflux.t6_generator_lvl.habitat_lvl == 1 and conflux.mage_guild.mage_guild_lvl >= 2 and upg:
        if resourceCheck(conflux.t6_generator_lvl.cost[0][1], player):
            build(conflux.t6_generator_lvl.cost[0][1], player)
            conflux.t6_generator_lvl.habitat_lvl = 2
            buy_building(conflux.t6_generator_lvl.name, "conflux")
            print('Altar of Thought upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 31 Upg. Pyre
    if conflux.t7_generator_lvl.habitat_lvl == 1 and upg:
        if resourceCheck(conflux.t7_generator_lvl.cost[0][1], player):
            build(conflux.t7_generator_lvl.cost[0][1], player)
            conflux.t7_generator_lvl.habitat_lvl = 2
            buy_building(conflux.t7_generator_lvl.name, "conflux")
            print('Pyre upgraded!')
            return None
        else:
            print('Not enough resources!')
