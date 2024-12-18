"""Script containing Castle castle upgrade alghoritm"""
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


def castleUpgrade(player, castle):
    """
    Castle castle upgrade alghoritm.
    :param player: Player object
    :param castle: Castle object
    :return: None
    """

    cost = full_unit_cost(castle)
    if player.gold < (cost/3):
        print("Not enought gold for units, dont build anything")
        return None
    # ----------------------------HARDCODED ZONE-----------------------------------------------
    # Tavern
    if not castle.tavern.built:
        if resourceCheck(castle.tavern.cost[0], player):
            build(castle.tavern.cost[0], player)
            castle.tavern.built = True
            buy_building(castle.tavern.name, "castle")
            print('Tavern built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # Fort
    if castle.fort.fort_lvl == 0 and castle.tavern.built:
        if resourceCheck(castle.fort.cost[0][0], player):
            build(castle.fort.cost[0][0], player)
            castle.fort.built = True
            castle.fort.fort_lvl = 1
            buy_building(castle.fort.name, "castle")
            print('Fort lvl 1 built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # Guardhouse
    if castle.t1_generator_lvl.habitat_lvl == 0 and castle.fort.fort_lvl > 0:
        if resourceCheck(castle.t1_generator_lvl.cost[0][0], player):
            build(castle.t1_generator_lvl.cost[0][0], player)
            castle.t1_generator_lvl.habitat_lvl = 1
            buy_building(castle.t1_generator_lvl.name, "castle")
            print('Guardhouse built!')
            return None
        else:
            print('Not enough resources!')
            return None

            # Archers Tower
    if castle.t2_generator_lvl.habitat_lvl == 0 and castle.t1_generator_lvl.habitat_lvl >= 1:
        if resourceCheck(castle.t2_generator_lvl.cost[0][0], player):
            build(castle.t2_generator_lvl.cost[0][0], player)
            castle.t2_generator_lvl.habitat_lvl = 1
            buy_building(castle.t2_generator_lvl.name, "castle")
            print('Archers Tower built!')
            return None
        else:
            print('Not enough resources!')
            return None

            # Upg. Archers Tower
    if castle.t2_generator_lvl.habitat_lvl == 1:
        if resourceCheck(castle.t2_generator_lvl.cost[0][1], player):
            build(castle.t2_generator_lvl.cost[0][1], player)
            castle.t2_generator_lvl.habitat_lvl = 2
            buy_building(castle.t2_generator_lvl.name, "castle")
            print('Archers Tower upgraded!')
            return None
        else:
            print('Not enough resources!')
            return None

    # Town Hall
    if castle.tavern.built and castle.t2_generator_lvl.habitat_lvl >= 1 and castle.city_hall.city_hall_lvl == 0:
        if resourceCheck(castle.city_hall.cost[0][0], player):
            build(castle.city_hall.cost[0][0], player)
            castle.city_hall.city_hall_lvl = 1
            player.daily_income[0] += 500
            castle.city_hall.built = True
            buy_building(castle.city_hall.name, "castle")
            print('Town Hall built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # Blacksmith
    if not castle.blacksmith.built:
        if resourceCheck(castle.blacksmith.cost[0], player):
            build(castle.blacksmith.cost[0], player)
            castle.blacksmith.built = True
            buy_building(castle.blacksmith.name, "castle")
            print('Blacksmith built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # Barracks
    if castle.t4_generator_lvl.habitat_lvl == 0 and castle.t1_generator_lvl.habitat_lvl >= 1:
        if resourceCheck(castle.t4_generator_lvl.cost[0][0], player):
            build(castle.t4_generator_lvl.cost[0][0], player)
            castle.t4_generator_lvl.habitat_lvl = 1
            print('Barracks built!')
            buy_building(castle.t4_generator_lvl.name, "castle")
            return None
        else:
            print('Not enough resources!')
            return None

            # Griffin Tower
    if castle.t3_generator_lvl.habitat_lvl == 0 and castle.t4_generator_lvl.habitat_lvl >= 1:
        if resourceCheck(castle.t3_generator_lvl.cost[0][0], player):
            build(castle.t3_generator_lvl.cost[0][0], player)
            castle.t3_generator_lvl.habitat_lvl = 1
            print('Griffin Tower built!')
            buy_building(castle.t3_generator_lvl.name, "castle")
            return None
        else:
            print('Not enough resources!')
            return None

            # Mage Guild Level 1
    if castle.mage_guild.mage_guild_lvl == 0 and castle.t3_generator_lvl.habitat_lvl >= 1:
        if resourceCheck(castle.mage_guild.cost[0][0], player):
            build(castle.mage_guild.cost[0][0], player)
            castle.mage_guild.mage_guild_lvl = 1
            buy_building(castle.mage_guild.name, "castle")
            print('Mage Guild Level 1 built!')
            return None
        else:
            print('Not enough resources!')
            return None
    # ----------------------------HARDCODED ZONE-----------------------------------------------
    # [hab = build habitat], [upg = upgrade habitat], [wall = build/upgrade fort], [capi = build/upgrade city_hall], [MG_M = build Marketplace , upgrade/build mage_guild, build blacksmith], [builds = build other buildings]
    hab, upg, wall, capi, MG_M, builds = town_choice(player, castle)

    # ------------------------------------------------------------------------------------------
    # Citadel
    if castle.fort.fort_lvl == 1 and wall:
        if resourceCheck(castle.fort.cost[0][1], player):
            build(castle.fort.cost[0][1], player)
            castle.fort.fort_lvl = 2
            buy_building(castle.fort.name, "castle")
            print('Citadel built!')
            return None
        else:
            print('Not enough resources!')

            # Marketplace
    if not castle.marketplace.built and MG_M:
        if resourceCheck(castle.marketplace.cost[0], player):
            build(castle.marketplace.cost[0], player)
            castle.marketplace.built = True
            buy_building(castle.marketplace.name, "castle")
            print('Marketplace built!')
            return None
        else:
            print('Not enough resources!')

    # City Hall
    if castle.city_hall.city_hall_lvl == 1 and castle.marketplace.built and castle.blacksmith.built and castle.mage_guild.mage_guild_lvl >= 1:
        if resourceCheck(castle.city_hall.cost[0][1], player):
            build(castle.city_hall.cost[0][1], player)
            castle.city_hall.city_hall_lvl = 2
            player.daily_income[0] += 1000
            buy_building(castle.city_hall.name, "castle")
            print('City Hall built!')
            return None
        else:
            print('Not enough resources!')

    # Monastery
    if castle.t5_generator_lvl.habitat_lvl == 0 and castle.t1_generator_lvl.habitat_lvl >= 1 and castle.mage_guild.mage_guild_lvl >= 1 and hab:
        if resourceCheck(castle.t5_generator_lvl.cost[0][0], player):
            build(castle.t5_generator_lvl.cost[0][0], player)
            castle.t5_generator_lvl.habitat_lvl = 1
            buy_building(castle.t5_generator_lvl.name, "castle")
            print('Monastery built!')
            return None
        else:
            print('Not enough resources!')

            # Castle
    if castle.fort.fort_lvl == 2 and wall:
        if resourceCheck(castle.fort.cost[0][2], player):
            build(castle.fort.cost[0][2], player)
            castle.fort.fort_lvl = 3
            buy_building(castle.fort.name, "castle")
            print('Castle built!')
            return None
        else:
            print('Not enough resources!')

            # Capitol
    if castle.fort.fort_lvl == 3 and castle.city_hall.city_hall_lvl == 2 and capi:
        if resourceCheck(castle.city_hall.cost[0][2], player):
            build(castle.city_hall.cost[0][2], player)
            castle.city_hall.city_hall_lvl = 3
            player.daily_income[0] += 2000
            buy_building(castle.city_hall.name, "castle")
            print('Capitol built!')
            return None
        else:
            print('Not enough resources!')

    # Stables
    if not castle.stables.built and castle.t1_generator_lvl.habitat_lvl == 1 and builds and False:
        if resourceCheck(castle.stables.cost[0], player):
            build(castle.stables.cost[0], player)
            castle.stables.built = True
            buy_building(castle.stables.name, "castle")
            print('Stables built!')
            return None
        else:
            print('Not enough resources!')

            # Training Grounds
    if castle.stables.built and castle.t6_generator_lvl.habitat_lvl == 0 and hab:
        if resourceCheck(castle.t6_generator_lvl.cost[0][0], player):
            build(castle.t6_generator_lvl.cost[0][0], player)
            castle.t6_generator_lvl.habitat_lvl = 1
            buy_building(castle.t6_generator_lvl.name, "castle")
            print('Training Grounds built!')
            return None
        else:
            print('Not enough resources!')

            # Mage guild Level 2
    if castle.mage_guild.mage_guild_lvl == 1 and MG_M:
        if resourceCheck(castle.mage_guild.cost[0][1], player):
            build(castle.mage_guild.cost[0][1], player)
            castle.mage_guild.mage_guild_lvl = 2
            buy_building(castle.mage_guild.name, "castle")
            print('Mage guild Level 2!')
            return None
        else:
            print('Not enough resources!')

    # Upg. Guardhouse
    if castle.t1_generator_lvl.habitat_lvl == 1 and upg:
        if resourceCheck(castle.t1_generator_lvl.cost[0][1], player):
            build(castle.t1_generator_lvl.cost[0][1], player)
            castle.t1_generator_lvl.habitat_lvl = 2
            buy_building(castle.t1_generator_lvl.name, "castle")
            print('Guardhouse upgraded !')
            return None
        else:
            print('Not enough resources!')

            # Upg. Griffin Tower
    if castle.t3_generator_lvl.habitat_lvl == 1 and upg:
        if resourceCheck(castle.t3_generator_lvl.cost[0][1], player):
            build(castle.t3_generator_lvl.cost[0][1], player)
            castle.t3_generator_lvl.habitat_lvl = 2
            buy_building(castle.t3_generator_lvl.name, "castle")
            print('Griffin Tower upgraded!')
            return None
        else:
            print('Not enough resources!')

            # Upg. Barracks
    if castle.t4_generator_lvl.habitat_lvl == 1 and upg:
        if resourceCheck(castle.t4_generator_lvl.cost[0][1], player):
            build(castle.t4_generator_lvl.cost[0][1], player)
            castle.t4_generator_lvl.habitat_lvl = 2
            buy_building(castle.t4_generator_lvl.name, "castle")
            print('Barracks upgraded!')
            return None
        else:
            print('Not enough resources!')

            # Portal of Glory
    if castle.t6_generator_lvl.habitat_lvl >= 1 and castle.t7_generator_lvl.habitat_lvl == 0 and castle.t5_generator_lvl.habitat_lvl >= 1 and hab:
        if resourceCheck(castle.t7_generator_lvl.cost[0][0], player):
            build(castle.t7_generator_lvl.cost[0][0], player)
            castle.t7_generator_lvl.habitat_lvl = 1
            buy_building(castle.t7_generator_lvl.name, "castle")
            print('Portal of Glory built!')
            return None
        else:
            print('Not enough resources!')

            # Resource Silo
    if castle.resource_silo.built == False and castle.marketplace.built:
        if resourceCheck(castle.resource_silo.cost[0], player):
            build(castle.resource_silo.cost[0], player)
            castle.resource_silo.built = True
            player.daily_income[1] += 1
            player.daily_income[2] += 1
            buy_building(castle.resource_silo.name, "castle")
            print('Resource Silo built!')
            return None
        else:
            print('Not enough resources!')

    # Mage guild Level 3
    if castle.mage_guild.mage_guild_lvl == 2 and MG_M:
        if resourceCheck(castle.mage_guild.cost[0][2], player):
            build(castle.mage_guild.cost[0][2], player)
            castle.mage_guild.mage_guild_lvl = 3
            buy_building(castle.mage_guild.name, "castle")
            print('Mage guild Level 3!')
            return None
        else:
            print('Not enough resources!')

            # Upg. Monastery
    if castle.mage_guild.mage_guild_lvl >= 1 and castle.t5_generator_lvl.habitat_lvl == 1 and upg:
        if resourceCheck(castle.t5_generator_lvl.cost[0][1], player):
            build(castle.t5_generator_lvl.cost[0][1], player)
            castle.t5_generator_lvl.habitat_lvl = 2
            buy_building(castle.t5_generator_lvl.name, "castle")
            print('Monastery upgraded!')
            return None
        else:
            print('Not enough resources!')

            # Griffin Bastion
    if castle.t3_generator_lvl.habitat_lvl >= 1 and castle.griffin_bastion.built == False and builds:
        if resourceCheck(castle.griffin_bastion.cost[0], player):
            build(castle.griffin_bastion.cost[0], player)
            castle.griffin_bastion.built = True
            buy_building(castle.griffin_bastion.name, "castle")
            print('Griffin Bastion built!')
            return None
        else:
            print('Not enough resources!')

            # Brotherhood of The Sword
    if castle.tavern.built and castle.brotherhood_of_the_sword.built == False and builds:
        if resourceCheck(castle.brotherhood_of_the_sword.cost[0], player):
            build(castle.brotherhood_of_the_sword.cost[0], player)
            castle.brotherhood_of_the_sword.built = True
            buy_building(castle.brotherhood_of_the_sword.name, "castle")
            print('Brotherhood of The Sword built!')
            return None
        else:
            print('Not enough resources!')

            # Upg. Training Grounds
    if castle.t6_generator_lvl.habitat_lvl == 1 and upg:
        if resourceCheck(castle.t6_generator_lvl.cost[0][1], player):
            build(castle.t6_generator_lvl.cost[0][1], player)
            castle.t6_generator_lvl.habitat_lvl = 2
            buy_building(castle.t6_generator_lvl.name, "castle")
            print('Training Grounds upgraded!')
            return None
        else:
            print('Not enough resources!')

    # Mage guild Level 4
    if castle.mage_guild.mage_guild_lvl == 3 and MG_M:
        if resourceCheck(castle.mage_guild.cost[0][3], player):
            build(castle.mage_guild.cost[0][3], player)
            castle.mage_guild.mage_guild_lvl = 4
            buy_building(castle.mage_guild.name, "castle")
            print('Mage guild Level 4!')
            return None
        else:
            print('Not enough resources!')

    # Upg. Portal of Glory
    if castle.t7_generator_lvl.habitat_lvl == 1 and upg:
        if resourceCheck(castle.t7_generator_lvl.cost[0][1], player):
            build(castle.t7_generator_lvl.cost[0][1], player)
            castle.t7_generator_lvl.habitat_lvl = 2
            buy_building(castle.t7_generator_lvl.name, "castle")
            print('Portal of Glory upgraded!')
            return None
        else:
            print('Not enough resources!')
