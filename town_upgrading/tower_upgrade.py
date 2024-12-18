"""Script containing Tower castle upgrade alghoritm"""
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


def towerUpgrade(player, tower):
    """
    Tower castle upgrade alghoritm.
    :param player: Player object
    :param tower: Tower object
    :return: None
    """
    cost = full_unit_cost(tower)
    if player.gold < (cost/3):
        print("Not enought gold for units, dont build anything")
        return None
    # ----------------------------HARDCODED ZONE-----------------------------------------------
    # tavern
    if not tower.tavern.built:
        if resourceCheck(tower.tavern.cost[0], player):
            build(tower.tavern.cost[0], player)
            tower.tavern.built = True
            buy_building(tower.tavern.name, "tower")
            print('Tavern built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # fort
    if tower.fort.fort_lvl == 0 and tower.tavern.built:
        if resourceCheck(tower.fort.cost[0][0], player):
            build(tower.fort.cost[0][0], player)
            tower.fort.fort_lvl = 1
            buy_building(tower.fort.name, "tower")
            print('Fort lvl 1 built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # workshop
    if tower.t1_generator_lvl.habitat_lvl==0 and tower.fort.fort_lvl >= 1:
        if resourceCheck(tower.t1_generator_lvl.cost[0][0], player):
            build(tower.t1_generator_lvl.cost[0][0], player)
            tower.t1_generator_lvl.habitat_lvl=1
            buy_building(tower.t1_generator_lvl.name, "tower")
            print('Workshop built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # parapet
    if tower.t1_generator_lvl.habitat_lvl>=1 and tower.t2_generator_lvl.habitat_lvl==0:
        if resourceCheck(tower.t2_generator_lvl.cost[0][0], player):
            build(tower.t2_generator_lvl.cost[0][0], player)
            tower.t2_generator_lvl.habitat_lvl =1
            buy_building(tower.t2_generator_lvl.name, "tower")
            print('Parapet built!')
            return None
        else:
            print('Not enough resources')
            return None

    # golem factory
    if tower.t3_generator_lvl.habitat_lvl == 0 and tower.t1_generator_lvl.habitat_lvl>=1 and tower.t2_generator_lvl.habitat_lvl>=1:
        if resourceCheck(tower.t3_generator_lvl.cost[0][0], player):
            build(tower.t3_generator_lvl.cost[0][0], player)
            tower.t3_generator_lvl.habitat_lvl=1
            buy_building(tower.t3_generator_lvl.name, "tower")
            print('Golem factory built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # town hall
    if tower.city_hall.city_hall_lvl==0 and tower.city_hall.city_hall_lvl == 0 and tower.t3_generator_lvl.habitat_lvl>=1:
        if resourceCheck(tower.city_hall.cost[0][0], player):
            build(tower.city_hall.cost[0][0], player)
            tower.city_hall.city_hall_lvl = 1
            player.daily_income[0] += 500
            buy_building(tower.city_hall.name, "tower")
            print('City hall built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # mage guild
    if tower.city_hall.city_hall_lvl >= 1 and tower.mage_guild.mage_guild_lvl == 0:
        if resourceCheck(tower.mage_guild.cost[0][0], player):
            build(tower.mage_guild.cost[0][0], player)
            tower.mage_guild.mage_guild_lvl = 1
            buy_building(tower.mage_guild.name, "tower")
            print('Mage guild lvl 1 built!')
            return None
        else:
            print('Not enough resources!')
            return None

    # marketplace
    if tower.mage_guild.mage_guild_lvl >= 1 and tower.marketplace.built == False:
        if resourceCheck(tower.marketplace.cost[0], player):
            build(tower.marketplace.cost[0], player)
            tower.marketplace.built = True
            buy_building(tower.marketplace.name, "tower")
            print('Marketplace built!')
            return None
        else:
            print('Not enough resources!')
            return None
    # ----------------------------HARDCODED ZONE-----------------------------------------------
    # [hab = build habitat], [upg = upgrade habitat], [wall = build/upgrade fort], [capi = build/upgrade city_hall], [MG_M = build Marketplace , upgrade/build mage_guild, build blacksmith], [builds = build other buildings]
    hab, upg, wall, capi, MG_M, builds = town_choice(player, tower)

    # ------------------------------------------------------------------------------------------
    # blacksmith
    if not tower.blacksmith.built and MG_M:
        if resourceCheck(tower.blacksmith.cost[0], player):
            build(tower.blacksmith.cost[0], player)
            tower.blacksmith.built = True
            buy_building(tower.blacksmith.name, "tower")
            print('Blacksmith built!')
            return None
        else:
            print('Not enough resources!')

    # city hall
    if tower.city_hall.city_hall_lvl == 1 and tower.blacksmith.built and tower.marketplace.built and tower.mage_guild.mage_guild_lvl>=1 and capi:
        if resourceCheck(tower.city_hall.cost[0][1], player):
            build(tower.city_hall.cost[0][1], player)
            tower.city_hall.city_hall_lvl = 2
            player.daily_income[0] += 1000
            buy_building(tower.city_hall.name, "tower")
            print('City hall built!')
            return None
        else:
            print('Not enough resources!')

    # Citadel
    if tower.fort.fort_lvl == 1 and wall:
        if resourceCheck(tower.fort.cost[0][1], player):
            build(tower.fort.cost[0][1], player)
            tower.fort.fort_lvl = 2
            buy_building(tower.fort.name, "tower")
            print('Citadel built!')
            return None
        else:
            print('Not enough resources!')

    # mage tower
    if tower.mage_guild.mage_guild_lvl>=1 and tower.t4_generator_lvl.habitat_lvl==0 and tower.t2_generator_lvl.habitat_lvl>=1 and tower.t3_generator_lvl.habitat_lvl>=1 and hab:
        if resourceCheck(tower.t4_generator_lvl.cost[0][0], player):
            build(tower.t4_generator_lvl.cost[0][0], player)
            tower.t4_generator_lvl.habitat_lvl=1
            buy_building(tower.t4_generator_lvl.name, "tower")
            print('Mage tower built!')
            return None
        else:
            print('Not enough resources!')

    # castle
    if tower.fort.fort_lvl == 2 and capi:
        if resourceCheck(tower.fort.cost[0][2], player):
            build(tower.fort.cost[0][2], player)
            tower.fort.fort_lvl = 3
            buy_building(tower.fort.name, "tower")
            print('Castle built!')
            return None
        else:
            print('Not enough resources!')

    # capitol
    if tower.fort.fort_lvl == 3 and tower.city_hall.city_hall_lvl == 2 and capi:
        if resourceCheck(tower.city_hall.cost[0][2], player):
            build(tower.city_hall.cost[0][2], player)
            tower.city_hall.city_hall_lvl = 3
            player.daily_income[0] += 2000
            buy_building(tower.city_hall.name, "tower")
            print('Capitol built!')
            return None
        else:
            print('Not enough resources!')

    # altar of wishes
    if tower.t5_generator_lvl.habitat_lvl==0 and tower.t4_generator_lvl.habitat_lvl>=1 and hab:
        if resourceCheck(tower.t5_generator_lvl.cost[0][0], player):
            build(tower.t5_generator_lvl.cost[0][0], player)
            tower.t5_generator_lvl.habitat_lvl=1
            buy_building(tower.t5_generator_lvl.name, "tower")
            print('Altar of wishes built!')
            return None
        else:
            print('Not enough resources!')

    # golden pavilion
    if tower.t6_generator_lvl.habitat_lvl==0 and tower.t4_generator_lvl.habitat_lvl>=1 and hab:
        if resourceCheck(tower.t6_generator_lvl.cost[0][0], player):
            build(tower.t6_generator_lvl.cost[0][0], player)
            tower.t6_generator_lvl.habitat_lvl=1
            buy_building(tower.t6_generator_lvl.name, "tower")
            print('Golden pavilion built!')
            return None
        else:
            print('Not enough resources!')

    # mage guild lvl 2
    if tower.mage_guild.mage_guild_lvl == 1 and MG_M:
        if resourceCheck(tower.mage_guild.cost[0][1], player):
            build(tower.mage_guild.cost[0][1], player)
            tower.mage_guild.mage_guild_lvl = 2
            buy_building(tower.mage_guild.name, "tower")
            print('Mage guild lvl 2 built!')
            return None
        else:
            print('Not enough resources!')

    # mage guild lvl 3
    if tower.mage_guild.mage_guild_lvl == 2 and MG_M:
        if resourceCheck(tower.mage_guild.cost[0][2], player):
            build(tower.mage_guild.cost[0][2], player)
            tower.mage_guild.mage_guild_lvl = 3
            buy_building(tower.mage_guild.name, "tower")
            print('Mage guild lvl 3 built!')
            return None
        else:
            print('Not enough resources!')

    # wall of knowledge
    if tower.mage_guild.mage_guild_lvl >= 1 and tower.wall_of_knowledge.built == False and builds and False:
        if resourceCheck(tower.wall_of_knowledge.cost[0], player):
            build(tower.wall_of_knowledge.cost[0], player)
            tower.wall_of_knowledge.built = True
            buy_building(tower.wall_of_knowledge.name, "tower")
            print('Wall of knowledge built!')
            return None
        else:
            print('Not enough resources!')

    # Upg. Parapet
    if tower.t2_generator_lvl.habitat_lvl==1 and upg:
        if resourceCheck(tower.t2_generator_lvl.cost[0][1], player):
            build(tower.t2_generator_lvl.cost[0][1], player)
            tower.t2_generator_lvl.habitat_lvl=2
            buy_building(tower.t2_generator_lvl.name, "tower")
            print('Parapet upgraded!')
            return None
        else:
            print('Not enough resources!')

    # Upg. Workshop
    if tower.t1_generator_lvl.habitat_lvl==1 and upg:
        if resourceCheck(tower.t1_generator_lvl.cost[0][1], player):
            build(tower.t1_generator_lvl.cost[0][1], player)
            tower.t1_generator_lvl.habitat_lvl=2
            buy_building(tower.t1_generator_lvl.name, "tower")
            print('Workshop upgraded!')
            return None
        else:
            print('Not enough resources!')

    # Upg. golem factory
    if tower.t3_generator_lvl.habitat_lvl==1 and upg:
        if resourceCheck(tower.t3_generator_lvl.cost[0][1], player):
            build(tower.t3_generator_lvl.cost[0][1], player)
            tower.t3_generator_lvl.habitat_lvl=2
            buy_building(tower.t3_generator_lvl.name, "tower")
            print('Golem factory upgraded!')
            return None
        else:
            print('Not enough resources!')

    # Library
    if tower.mage_guild.mage_guild_lvl>=1 and tower.library.built == False and builds:
        if resourceCheck(tower.library.cost[0], player):
            build(tower.library.cost[0], player)
            tower.library.built = True
            buy_building(tower.library.name, "tower")
            print('Library built!')
            return None
        else:
            print('Not enough resources!')

    # Upg Mage tower
    if tower.t4_generator_lvl.habitat_lvl==1 and tower.library.built and upg:
        if resourceCheck(tower.t4_generator_lvl.cost[0][1], player):
            build(tower.t4_generator_lvl.cost[0][1], player)
            tower.t4_generator_lvl.habitat_lvl=2
            buy_building(tower.t4_generator_lvl.name, "tower")
            print('Mage Tower Upgraded!')
            return None
        else:
            print('Not enough resources!')

    # lookout tower
    if tower.lookout_tower.built == False and tower.fort.fort_lvl >= 1 and builds:
        if resourceCheck(tower.lookout_tower.cost[0], player):
            build(tower.lookout_tower.cost[0], player)
            tower.lookout_tower.built = True
            buy_building(tower.lookout_tower.name, "tower")
            print('Lookout tower built!')
            return None
        else:
            print('Not enough resources!')

    # Upg. Altar of wishes
    if tower.t5_generator_lvl.habitat_lvl==1 and upg:
        if resourceCheck(tower.t5_generator_lvl.cost[0][1], player):
            build(tower.t5_generator_lvl.cost[0][1], player)
            tower.t5_generator_lvl.habitat_lvl=2
            buy_building(tower.t5_generator_lvl.name, "tower")
            print('Altar of wishes upgraded!')
            return None
        else:
            print('Not enough resources!')

    # cloud temple
    if tower.t7_generator_lvl.habitat_lvl==0 and tower.t5_generator_lvl.habitat_lvl>=1 and tower.t6_generator_lvl.habitat_lvl>=1 and hab:
        if resourceCheck(tower.t7_generator_lvl.cost[0][0], player):
            build(tower.t7_generator_lvl.cost[0][0], player)
            tower.t7_generator_lvl.habitat_lvl=1
            buy_building(tower.t7_generator_lvl.name, "tower")
            print('Cloud temple built!')
            return None
        else:
            print('Not enough resources!')

    # Upg. cloud temple
    if tower.t7_generator_lvl.habitat_lvl==1 and upg:
        if resourceCheck(tower.t7_generator_lvl.cost[0][1], player):
            build(tower.t7_generator_lvl.cost[0][1], player)
            tower.t7_generator_lvl.habitat_lvl=2
            buy_building(tower.t7_generator_lvl.name, "tower")
            print('Cloud temple upgraded!')
            return None
        else:
            print('Not enough resources!')

    # Upg. golden pavilion
    if tower.t6_generator_lvl.habitat_lvl==1 and upg:
        if resourceCheck(tower.t6_generator_lvl.cost[0][0], player):
            build(tower.t6_generator_lvl.cost[0][1], player)
            tower.t6_generator_lvl.habitat_lvl=2
            buy_building(tower.t6_generator_lvl.name, "tower")
            print('Golden pavilion upgraded!')
            return None
        else:
            print('Not enough resources!')

    # Mage guild lvl 4
    if tower.mage_guild.mage_guild_lvl == 3 and MG_M:
        if resourceCheck(tower.mage_guild.cost[0][3], player):
            build(tower.mage_guild.cost[0][3], player)
            tower.mage_guild.mage_guild_lvl = 4
            buy_building(tower.mage_guild.name, "tower")
            print('Mage guild lvl 4!')
            return None
        else:
            print('Not enough resources!')

    # mage guild lvl 5
    if tower.mage_guild.mage_guild_lvl == 4 and MG_M:
        if resourceCheck(tower.mage_guild.cost[0][4], player):
            build(tower.mage_guild.cost[0][4], player)
            tower.mage_guild.mage_guild_lvl = 5
            buy_building(tower.mage_guild.name, "tower")
            print('Mage guild lvl 5!')
            return None
        else:
            print('Not enough resources!')

    # sculptors wings
    if tower.sculptor_wings.built == False and tower.t2_generator_lvl.habitat_lvl>=1 and builds:
        if resourceCheck(tower.sculptor_wings.cost[0], player):
            build(tower.sculptor_wings.cost[0], player)
            tower.sculptor_wings.built = True
            buy_building(tower.sculptor_wings.name, "tower")
            print('Sculptors Wings built!')
            return None
        else:
            print('Not enough resources!')

    # resource silo
    if tower.resource_silo.built == False and tower.marketplace.built:
        if resourceCheck(tower.resource_silo.cost[0], player):
            build(tower.resource_silo.cost[0], player)
            tower.resource_silo.built = True
            player.daily_income[6] += 1
            buy_building(tower.resource_silo.name, "tower")
            print('Resource Silo built!')
            return None
        else:
            print('Not enough resources!')

    # artifact merchant
    if tower.artifact_merchant.built == False and tower.marketplace.built and builds:
        if resourceCheck(tower.artifact_merchant.cost[0], player):
            build(tower.artifact_merchant.cost[0], player)
            tower.artifact_merchant.built = True
            buy_building(tower.artifact_merchant.name, "tower")
            print('Artifact merchant build!')
            return None
        else:
            print('Not enough resources!')
