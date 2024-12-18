"""Script containing Dungeon castle upgrade alghoritm"""
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


def dungeonUpgrade(player, dungeon):
    """
    Dungeon castle upgrade alghoritm.
    :param player: Player object
    :param dungeon: Dungeon object
    :return: None
    """
    cost = full_unit_cost(dungeon)
    if player.gold < (cost/3):
        print("Not enought gold for units, dont build anything")
        return None
    # ----------------------------HARDCODED ZONE-----------------------------------------------
    # 1 Tavern
    if not dungeon.tavern.built:
        if resourceCheck(dungeon.tavern.cost[0], player):
            build(dungeon.tavern.cost[0], player)
            buy_building(dungeon.tavern.name,"dungeon")
            dungeon.tavern.built = True
            print('Tavern built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 2 Fort
    if dungeon.tavern.built and dungeon.fort.fort_lvl < 1:
        if resourceCheck(dungeon.fort.cost[0][0], player):
            build(dungeon.fort.cost[0][0], player)
            buy_building(dungeon.fort.name, "dungeon")
            dungeon.fort.built = True
            dungeon.fort.fort_lvl = 1
            print('Fort Level 1 built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 3 Warren
    if dungeon.fort.fort_lvl == 1 and dungeon.t1_generator_lvl.habitat_lvl == 0:
        if resourceCheck(dungeon.t1_generator_lvl.cost[0][0], player):
            build(dungeon.t1_generator_lvl.cost[0][0], player)
            buy_building(dungeon.t1_generator_lvl.name, "dungeon")
            dungeon.t1_generator_lvl.habitat_lvl = 1
            print('Warren built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 4 Pillar of Eyes
    if dungeon.t3_generator_lvl.habitat_lvl == 0 and dungeon.t1_generator_lvl.habitat_lvl >= 1:
        if resourceCheck(dungeon.t3_generator_lvl.cost[0][0], player):
            build(dungeon.t3_generator_lvl.cost[0][0], player)
            buy_building(dungeon.t3_generator_lvl.name, "dungeon")
            dungeon.t3_generator_lvl.habitat_lvl = 1
            print('Pillar of Eyes built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 5 Harpy Loft
    if dungeon.t2_generator_lvl.habitat_lvl == 0 and dungeon.t3_generator_lvl.habitat_lvl >= 1:
        if resourceCheck(dungeon.t2_generator_lvl.cost[0][0], player):
            build(dungeon.t2_generator_lvl.cost[0][0], player)
            buy_building(dungeon.t2_generator_lvl.name, "dungeon")
            dungeon.t2_generator_lvl.habitat_lvl = 1
            print('Harpy Loft built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 6 Town Hall
    if dungeon.city_hall.city_hall_lvl <= 0:
        if resourceCheck(dungeon.city_hall.cost[0][0], player):
            build(dungeon.city_hall.cost[0][0], player)
            buy_building(dungeon.city_hall.name, "dungeon")
            dungeon.city_hall.city_hall_lvl = 1
            player.daily_income[0] += 500
            print('Town Hall built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 7 Mage Guild Level 1
    if dungeon.mage_guild.mage_guild_lvl < 1:
        if resourceCheck(dungeon.mage_guild.cost[0][0], player):
            build(dungeon.mage_guild.cost[0][0], player)
            buy_building(dungeon.mage_guild.name, "dungeon")
            dungeon.mage_guild.mage_guild_lvl = 1
            print('Mage Guild Level 1!')
            return None
        else:
            print('Not enough resources!')
            return None

    # 8 Marketplace
    if dungeon.mage_guild.mage_guild_lvl >= 1 and not dungeon.marketplace.built:
        if resourceCheck(dungeon.marketplace.cost[0], player):
            build(dungeon.marketplace.cost[0], player)
            buy_building(dungeon.marketplace.name, "dungeon")
            dungeon.marketplace.built = True
            print('Marketplace built!')
            return None
        else:
            print('Not enough resources!')
            return None
    # ----------------------------HARDCODED ZONE-----------------------------------------------
    # [hab = build habitat], [upg = upgrade habitat], [wall = build/upgrade fort], [capi = build/upgrade city_hall], [MG_M = build Marketplace , upgrade/build mage_guild, build blacksmith], [builds = build other buildings]
    hab, upg, wall, capi, MG_M, builds = town_choice(player, dungeon)

    # ------------------------------------------------------------------------------------------
    # 9 Blacksmith
    if not dungeon.blacksmith.built and MG_M:
        if resourceCheck(dungeon.blacksmith.cost[0], player):
            build(dungeon.blacksmith.cost[0], player)
            buy_building(dungeon.blacksmith.name, "dungeon")
            dungeon.blacksmith.built = True
            print('Blacksmith built!')
            return None
        else:
            print('Not enough resources!')

    # 10 City Hall
    if dungeon.city_hall.city_hall_lvl == 1 and dungeon.marketplace.built and dungeon.blacksmith.built and dungeon.mage_guild.mage_guild_lvl >= 1 and capi:
        if resourceCheck(dungeon.city_hall.cost[0][1], player):
            build(dungeon.city_hall.cost[0][1], player)
            buy_building(dungeon.city_hall.name, "dungeon")
            dungeon.city_hall.city_hall_lvl = 2
            player.daily_income[0] += 1000
            print('City Hall built!')
            return None
        else:
            print('Not enough resources!')

    # 11 Upg. Pillar of Eyes
    if dungeon.t3_generator_lvl.habitat_lvl == 1 and upg:
        if resourceCheck(dungeon.t3_generator_lvl.cost[0][1], player):
            build(dungeon.t3_generator_lvl.cost[0][1], player)
            buy_building(dungeon.t3_generator_lvl.name, "dungeon")
            dungeon.t3_generator_lvl.habitat_lvl = 2
            print('Pillar of Eyes upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 12 Citadel
    if dungeon.fort.fort_lvl == 1 and wall:
        if resourceCheck(dungeon.fort.cost[0][1], player):
            build(dungeon.fort.cost[0][1], player)
            buy_building(dungeon.fort.name, "dungeon")
            dungeon.fort.fort_lvl = 2
            print('Citadel built!')
            return None
        else:
            print('Not enough resources!')

    # 13 Upg. Harpy Loft
    if dungeon.t2_generator_lvl.habitat_lvl == 1 and upg:
        if resourceCheck(dungeon.t2_generator_lvl.cost[0][1], player):
            build(dungeon.t2_generator_lvl.cost[0][1], player)
            buy_building(dungeon.t2_generator_lvl.name, "dungeon")
            dungeon.t2_generator_lvl.habitat_lvl = 2
            print('Harpy Loft upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 14 Chapel of Stilled Voices
    if dungeon.t4_generator_lvl.habitat_lvl == 0 and dungeon.t2_generator_lvl.habitat_lvl >= 1 and dungeon.t3_generator_lvl.habitat_lvl >= 1 and hab:
        if resourceCheck(dungeon.t4_generator_lvl.cost[0][0], player):
            build(dungeon.t4_generator_lvl.cost[0][0], player)
            buy_building(dungeon.t4_generator_lvl.name, "dungeon")
            dungeon.t4_generator_lvl.habitat_lvl = 1
            print('Chapel of Stilled Voices built!')
            return None
        else:
            print('Not enough resources!')

    # 15 Labyrinth
    if dungeon.t5_generator_lvl.habitat_lvl == 0 and dungeon.t4_generator_lvl.habitat_lvl >= 1 and hab:
        if resourceCheck(dungeon.t5_generator_lvl.cost[0][0], player):
            build(dungeon.t5_generator_lvl.cost[0][0], player)
            buy_building(dungeon.t5_generator_lvl.name, "dungeon")
            dungeon.t5_generator_lvl.habitat_lvl = 1
            print('Labyrinth built!')
            return None
        else:
            print('Not enough resources!')

    # 16 Castle
    if dungeon.fort.fort_lvl == 2 and wall:
        if resourceCheck(dungeon.fort.cost[0][2], player):
            build(dungeon.fort.cost[0][2], player)
            buy_building(dungeon.fort.name, "dungeon")
            dungeon.fort.fort_lvl = 3
            print('Castle built!')
            return None
        else:
            print('Not enough resources!')

    # 17 Capitol
    if dungeon.city_hall.city_hall_lvl == 2 and dungeon.fort.fort_lvl == 3 and capi:
        if resourceCheck(dungeon.city_hall.cost[0][2], player):
            build(dungeon.city_hall.cost[0][2], player)
            buy_building(dungeon.city_hall.name, "dungeon")
            dungeon.city_hall.city_hall_lvl = 3
            player.daily_income[0] += 2000
            print('Capitol built!')
            return None
        else:
            print('Not enough resources!')

    # 18 Manticore Lair
    if dungeon.t6_generator_lvl.habitat_lvl == 0 and dungeon.t4_generator_lvl.habitat_lvl >= 1 and hab:
        if resourceCheck(dungeon.t6_generator_lvl.cost[0][0], player):
            build(dungeon.t6_generator_lvl.cost[0][0], player)
            buy_building(dungeon.t6_generator_lvl.name, "dungeon")
            dungeon.t6_generator_lvl.habitat_lvl = 1
            print('Manticore Lair built!')
            return None
        else:
            print('Not enough resources!')

    # 19 Mage guild Level 2
    if dungeon.mage_guild.mage_guild_lvl == 1 and MG_M:
        if resourceCheck(dungeon.mage_guild.cost[0][1], player):
            build(dungeon.mage_guild.cost[0][1], player)
            buy_building(dungeon.mage_guild.name, "dungeon")
            dungeon.mage_guild.mage_guild_lvl = 2
            print('Mage guild Level 2!')
            return None
        else:
            print('Not enough resources!')

    # 20 Mage guild Level 3
    if dungeon.mage_guild.mage_guild_lvl == 2 and MG_M:
        if resourceCheck(dungeon.mage_guild.cost[0][2], player):
            build(dungeon.mage_guild.cost[0][2], player)
            buy_building(dungeon.mage_guild.name, "dungeon")
            dungeon.mage_guild.mage_guild_lvl = 3
            print('Mage guild Level 3!')
            return None
        else:
            print('Not enough resources!')

    # 21 Upg. Warren
    if dungeon.t1_generator_lvl.habitat_lvl == 1 and upg:
        if resourceCheck(dungeon.t1_generator_lvl.cost[0][1], player):
            build(dungeon.t1_generator_lvl.cost[0][1], player)
            buy_building(dungeon.t1_generator_lvl.name, "dungeon")
            dungeon.t1_generator_lvl.habitat_lvl = 2
            print('Warren upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 22 Mage guild Level 4
    if dungeon.mage_guild.mage_guild_lvl == 3 and MG_M:
        if resourceCheck(dungeon.mage_guild.cost[0][3], player):
            build(dungeon.mage_guild.cost[0][3], player)
            buy_building(dungeon.mage_guild.name, "dungeon")
            dungeon.mage_guild.mage_guild_lvl = 4
            print('Mage guild Level 4!')
            return None
        else:
            print('Not enough resources!')

    # 23 Battle Scholar Academy
    if not dungeon.battle_scholar_academy.built and builds and False:
        if resourceCheck(dungeon.battle_scholar_academy.cost[0], player):
            build(dungeon.battle_scholar_academy.cost[0], player)
            buy_building(dungeon.battle_scholar_academy.name, "dungeon")
            dungeon.battle_scholar_academy.built = True
            print('Battle Scholar Academy built!')
            return None
        else:
            print('Not enough resources!')

    # 24 Upg. Chapel of Stilled Voices
    if dungeon.t4_generator_lvl.habitat_lvl == 1 and upg:
        if resourceCheck(dungeon.t4_generator_lvl.cost[0][1], player):
            build(dungeon.t4_generator_lvl.cost[0][1], player)
            buy_building(dungeon.t4_generator_lvl.name, "dungeon")
            dungeon.t4_generator_lvl.habitat_lvl = 2
            print('Chapel of Stilled Voices upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 25 Dragon Cave
    if dungeon.t7_generator_lvl.habitat_lvl == 0 and dungeon.mage_guild.mage_guild_lvl >= 2 and dungeon.t6_generator_lvl.habitat_lvl >= 1 and hab:
        if resourceCheck(dungeon.t7_generator_lvl.cost[0][0], player):
            build(dungeon.t7_generator_lvl.cost[0][0], player)
            buy_building(dungeon.t7_generator_lvl.name, "dungeon")
            dungeon.t7_generator_lvl.habitat_lvl = 1
            print('Dragon Cave built!')
            return None
        else:
            print('Not enough resources!')

    # 26 Upg. Labyrinth
    if dungeon.t5_generator_lvl.habitat_lvl == 1 and upg:
        if resourceCheck(dungeon.t5_generator_lvl.cost[0][1], player):
            build(dungeon.t5_generator_lvl.cost[0][1], player)
            buy_building(dungeon.t5_generator_lvl.name, "dungeon")
            dungeon.t5_generator_lvl.habitat_lvl = 2
            print('Labyrinth upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 27 Upg. Manticore Lair
    if dungeon.t6_generator_lvl.habitat_lvl == 1 and upg:
        if resourceCheck(dungeon.t6_generator_lvl.cost[0][1], player):
            build(dungeon.t6_generator_lvl.cost[0][1], player)
            buy_building(dungeon.t6_generator_lvl.name, "dungeon")
            dungeon.t6_generator_lvl.habitat_lvl = 2
            print('Manticore Lair upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 28 Mage Guild Level 5
    if dungeon.mage_guild.mage_guild_lvl == 4 and MG_M:
        if resourceCheck(dungeon.mage_guild.cost[0][4], player):
            build(dungeon.mage_guild.cost[0][4], player)
            buy_building(dungeon.mage_guild.name, "dungeon")
            dungeon.mage_guild.mage_guild_lvl = 5
            print('Mage Guild Level 5!')
            return None
        else:
            print('Not enough resources!')

    # 29 Upg. Dragon Cave
    if dungeon.t7_generator_lvl.habitat_lvl == 1 and dungeon.mage_guild.mage_guild_lvl >= 3 and upg:
        if resourceCheck(dungeon.t7_generator_lvl.cost[0][1], player):
            build(dungeon.t7_generator_lvl.cost[0][1], player)
            buy_building(dungeon.t7_generator_lvl.name, "dungeon")
            dungeon.t7_generator_lvl.habitat_lvl = 2
            print('Upg. Dragon Cave upgraded!')
            return None
        else:
            print('Not enough resources!')

    # 30 Portal of Summoning
    if not dungeon.portal_of_summoning.built and builds:
        if resourceCheck(dungeon.portal_of_summoning.cost[0], player):
            build(dungeon.portal_of_summoning.cost[0], player)
            buy_building(dungeon.portal_of_summoning.name, "dungeon")
            dungeon.portal_of_summoning.built = True
            print('Portal of Summoning built')
            return None
        else:
            print('Not enough resources!')

    # 31 Mana Vortex
    if not dungeon.mana_vortex.built and dungeon.mage_guild.mage_guild_lvl>=1 and builds:
        if resourceCheck(dungeon.mana_vortex.cost[0], player):
            build(dungeon.mana_vortex.cost[0], player)
            buy_building(dungeon.mana_vortex.name, "dungeon")
            dungeon.mana_vortex.built = True
            print('Mana Vortex built')
            return None
        else:
            print('Not enough resources!')

    # 32 Mushroom Rings
    if not dungeon.mushroom_rings.built and dungeon.t1_generator_lvl.habitat_lvl >= 1 and builds:
        if resourceCheck(dungeon.mushroom_rings.cost[0], player):
            build(dungeon.mushroom_rings.cost[0], player)
            buy_building(dungeon.mushroom_rings.name, "dungeon")
            dungeon.mushroom_rings.built = True
            print("Mushroom Rings built")
            return None
        else:
            print('Not enough resources!')

    # 33 Resource Silo
    if not dungeon.resource_silo.built and dungeon.marketplace.built:
        if resourceCheck(dungeon.resource_silo.cost[0], player):
            build(dungeon.resource_silo.cost[0], player)
            buy_building(dungeon.resource_silo.name, "dungeon")
            dungeon.resource_silo.built = True
            player.daily_income[4] += 1
            print('Resource Silo built!')
            return None
        else:
            print('Not enough resources!')

    # 34 Artifact Merchants
    if not dungeon.artifact_merchant.built and dungeon.marketplace.built and builds:
        if resourceCheck(dungeon.artifact_merchant.cost[0], player):
            build(dungeon.artifact_merchant.cost[0], player)
            buy_building(dungeon.artifact_merchant.name, "dungeon")
            dungeon.artifact_merchant.built = True
            print("Artifact Merchants built")
            return None
        else:
            print('Not enough resources!')
