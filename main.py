from image_processing import screen_slicing
from image_processing.adventure_image_processing import remove_lost_cities, find_heroes
import GUI_handling.AdventureGUI
import image_processing.hero_filling
import Adventure_AI.AdventureAI as adv
from GUI_handling.TownGUI import hire_hero
from image_processing.blue_hero import check_if_blue_hero_exists, fill_enemy_hero
from town_upgrading.castle_upgrade import castleUpgrade
from town_upgrading.conflux_upgrade import confluxUpgrade
from town_upgrading.cove_upgrade import coveUpgrade
from town_upgrading.dungeon_upgrade import dungeonUpgrade
from town_upgrading.fortress_upgrade import fortressUpgrade
from town_upgrading.inferno_upgrade import infernoUpgrade
from town_upgrading.necropolis_upgrade import necropolisUpgrade
from town_upgrading.rampart_upgrade import rampartUpgrade
from town_upgrading.stronghold_upgrade import strongholdUpgrade
from town_upgrading.tower_upgrade import towerUpgrade
from data.player_data import Player
from data.hero import Hero, Slot, Slots, SecondarySkills, SecondarySkill
import data.classes_const as creatures
import time
from GUI_handling.AdventureGUI import enter_town, leave_screen
from path_finding_alghoritms.calculate_movments_points_at_start_day import \
    calculate_movments_points_at_start_day as movment
from image_processing.detecting_window import execute_detecting_enemy_turn


# def change_temp_values(map_obj, map_fog):
#     """
#
#     :param map_obj:
#     :param map_fog:
#     :return:
#     """
#     for y, row in enumerate(map_obj):
#         for x, tile in enumerate(row):
#             value = tile
#             if map_fog[y, x] == 0:
#                 map_obj[y, x] = terrain.fow
#
#             elif value == 0:
#                 map_obj[y, x] = terrain.Obstacle_terr
#             elif value == 1:
#                 map_obj[y, x] = terrain.Grass
#             elif value == 2:
#                 map_obj[y, x] = terrain.Dirt
#             elif value == 8:
#                 map_obj[y, x] = objects.Treasure_Chest


def leave_town():
    """
    someone wanted to have better name for function
    """
    leave_screen()


def read_hero(heroreader, player, n):
    """
    function for reading all available information about our hero

    :param heroreader: heroreader object
    :param player: player object
    :param n: number of hero on list
    """
    GUI_handling.AdventureGUI.press_hero(n)
    time.sleep(0.04)
    heroreader.find_all(player.heroes[n])  # find values of our first hero
    time.sleep(0.04)
    leave_town()
    time.sleep(0.04)


def read_army(heroreader, hero, i):
    """
    function to read army of our hero

    :param heroreader: heroreader object
    :param hero: hero to read
    :param i: number of hero on list
    """
    GUI_handling.AdventureGUI.press_hero(i)
    time.sleep(0.04)
    heroreader.find_units(hero)
    time.sleep(0.04)
    leave_town()
    time.sleep(0.04)


def build_building_in_town(player, city):
    """
    function checks what is the type of our city

    :param player: class Player
    :param city:
    """
    if city.name == "Castle":
        castleUpgrade(player, city)
    if city.name == "Rampart":
        rampartUpgrade(player, city)
    if city.name == "Tower":
        towerUpgrade(player, city)
    if city.name == "Inferno":
        infernoUpgrade(player, city)
    if city.name == "Necropolis":
        necropolisUpgrade(player, city)
    if city.name == "Dungeon":
        dungeonUpgrade(player, city)
    if city.name == "Stronghold":
        strongholdUpgrade(player, city)
    if city.name == "Fortress":
        fortressUpgrade(player, city)
    if city.name == "Conflux":
        confluxUpgrade(player, city)
    if city.name == "Cove":
        coveUpgrade(player, city)


def buy_hero(player, reader, type):
    """
    function to buy new hero

    :param player: player object
    :param reader: heroreader object
    :param type: type of hero main/not main
    """
    enter_town(0)
    time.sleep(0.1)
    GUI_handling.TownGUI.click_tavern(player.cities[0].name)
    time.sleep(0.1)
    GUI_handling.TownGUI.hire_hero(0)
    hero = Hero(1, type, 'Jenova', 1, 3, 1, 1, Slots(Slot(creatures.Centaur, 21), Slot(creatures.Dwarf, 5),
                                                     Slot(creatures.Wood_Elf, 2)),
                skills=SecondarySkills(SecondarySkill(2, 'Archery', 5)),
                heroclass='might')
    hero.position = (player.cities[0].position)
    player.heroes.append(hero)
    time.sleep(0.1)
    leave_town()
    time.sleep(0.1)
    read_hero(reader, player, len(player.heroes) - 1)


if __name__ == '__main__':

    read_cities = 1

    player = Player('Red', 20000, 20, 20, 10, 10, 10, 10)
    hero = Hero(1, 'main', 'Jenova', 1, 3, 1, 1, Slots(Slot(creatures.Centaur, 21), Slot(creatures.Dwarf, 5),
                                                       Slot(creatures.Wood_Elf, 2)),
                skills=SecondarySkills(SecondarySkill(2, 'Archery', 5)),
                heroclass='might')
    ranges = (
        (player.wood - 5, player.wood + 10),
        (player.mercury - 5, player.mercury + 10), (player.ore - 5, player.ore + 10),
        (player.sulfur - 5, player.sulfur + 10), (player.crystal - 5, player.crystal + 10),
        (player.gems - 5, player.gems + 10), (player.gold - 1000, player.gold + 10000))
    screen_slicing.check_resources(player, ranges)
    player.heroes.append(hero)
    player.heroes[0].position = (3, 4)
    advAI = adv.AdventureAI(player)
    heroreader = image_processing.hero_filling.Finder()
    # read_hero(heroreader, player, 0)
    debug = 'a'
    enter_town(0)
    time.sleep(0.1)
    GUI_handling.TownGUI.click_town_hall(faction=player.cities[0].name)
    time.sleep(0.1)
    player.cities[0].crop_building_names()
    time.sleep(0.5)
    leave_town()
    time.sleep(0.5)
    leave_town()
    time.sleep(0.5)
    for i, city in enumerate(player.cities):  # In every city we build building
        player.camera = city.position
        enter_town(i)
        time.sleep(0.5)
        build_building_in_town(player, city)
        time.sleep(0.08)
        leave_town()
        time.sleep(0.08)

    enter_town(0)
    time.sleep(0.1)
    player.cities[0].action(player, player.heroes[0])
    time.sleep(0.1)
    enter_town(0)

    time.sleep(0.1)
    # advAI.heroes[0].mspoints = 1900
    # advAI.playHeroDay()
    # enter_town(0)
    # time.sleep(0.04)
    GUI_handling.TownGUI.hero_garrison_change('bottom')
    time.sleep(0.1)
    GUI_handling.TownGUI.click_tavern(player.cities[0].name)
    time.sleep(0.1)
    hire_hero(0)
    # advAI.heroPointer = 1
    time.sleep(0.1)
    GUI_handling.TownGUI.hero_garrison_change('top')
    time.sleep(0.1)
    GUI_handling.TownGUI.move_all_units_to_other_side(1)
    time.sleep(0.1)
    for i in range(8, 16):
        GUI_handling.TownGUI.merge_stacks_unit(i)
        time.sleep(0.1)
    time.sleep(0.1)
    leave_town()
    time.sleep(0.1)
    advAI.heroPointer = 0
    read_hero(heroreader, player, 0)
    advAI.heroes[0].mspoints = movment(advAI.heroes[0])
    advAI.playHeroDay()
    time.sleep(0.1)
    enter_town(0)
    time.sleep(0.1)
    GUI_handling.TownGUI.hero_garrison_change('top')
    time.sleep(0.1)
    leave_town()
    advAI.heroPointer = 1
    player.heroes.append(Hero(1, 'not_main', 'Jenova', 1, 3, 1, 1))
    player.heroes[1].position = (3, 4)
    player.camera = (3, 4)
    time.sleep(0.1)
    read_hero(heroreader, player, 1)
    advAI.screen.hero_positions.append((3, 4, "Red"))
    advAI.heroes[1].mspoints = movment(advAI.heroes[1])
    time.sleep(0.1)
    advAI.screen.hero_positions.append((3, 4, 'Red'))
    advAI.playHeroDay()
    time.sleep(0.04)
    GUI_handling.AdventureGUI.end_turn()
    player.day += 1
    time.sleep(5)
    not_end = True
    for hero in player.heroes:
        hero.mspoints = movment(hero)
    after = image_processing.adventure_image_processing.check_if_hero_is_dead_first()
    while not_end:
        if len(player.cities) > read_cities:
            for i in range(read_cities - 1, len(player.cities)):
                enter_town(i)
                time.sleep(0.1)
                GUI_handling.TownGUI.click_town_hall(faction=player.cities[i].name)
                time.sleep(0.1)
                player.cities[i].crop_building_names()
                time.sleep(0.5)
                leave_town()
                time.sleep(0.5)
                leave_town()
            read_cities = i
        # Finding all the heroes, blue and red ones
        allTheHeroes = find_heroes(advAI.screen, advAI.map.obj)
        death = image_processing.adventure_image_processing.check_if_hero_is_dead_last_without_hero(after, player)
        if death:
            for hero in player.heroes:
                x, y = hero.position
                pos = (x, y, "Red")
                if pos not in allTheHeroes:
                    player.heroes.remove(hero)
        remove_lost_cities(player)
        # Actualize camera to the first hero at the start of the turn
        player.camera = player.heroes[0].position

        if len(player.heroes) < 2:
            # Actualize camera to the city position when we need to buy another hero
            player.camera = player.cities[0].position
            if player.heroes[0].herotype == "main":
                type = "not main"
            else:
                type = "main"
            buy_hero(player, heroreader, type)
        time.sleep(0.1)
        image_processing.adventure_image_processing.remove_dead_heroes(player)

        # Testing whether detected blue heroes exists at their position
        player.enemies = []
        for x, y, color in allTheHeroes:
            if color == "Blue":
                fill_enemy_hero(player, (x, y))

        ranges = ((player.wood - 5, player.wood + 10),
                  (player.mercury - 5, player.mercury + 10), (player.ore - 5, player.ore + 10),
                  (player.sulfur - 5, player.sulfur + 10),
                  (player.crystal - 5, player.crystal + 10), (player.gems - 5, player.gems + 10),
                  (player.gold - 1000, player.gold + 10000))
        screen_slicing.check_resources(player, ranges)

        # Finding whether we lost our mines
        for mine in player.captured_mines:
            # Checking color of the mine at the global map
            color = image_processing.adventure_image_processing.check_mine_owner_ocr(player, mine.position)[0]
            if color[0] != player.color:
                player.captured_mines.remove(mine)

                # Adding lost mine to goals
                advAI.addLostMineToGoals(mine)

        # if player.week == 1 and player.month == 1:
        for i, city in enumerate(player.cities):
            player.camera = city.position
            enter_town(i)
            time.sleep(0.08)
            build_building_in_town(player, city)
            time.sleep(0.08)
            leave_town()
            time.sleep(0.08)

        for i, hero in enumerate(player.heroes):
            advAI.heroPointer = i
            player.camera = hero.position
            GUI_handling.AdventureGUI.press_hero(i)
            time.sleep(0.08)
            read_army(heroreader, hero, i)
            time.sleep(0.08)
            advAI.playHeroDay()
        # else:
        #     for i, hero in enumerate(player.heroes):
        #         GUI_handling.AdventureGUI.press_hero(i)
        #         advAI.heroes[0].mspoints = 1500
        #         advAI.playHeroDay()
        #     for i, city in enumerate(player.cities):
        #         enter_town(i)
        #         time.sleep(0.04)
        #         build_building_in_town(player, city)
        #         time.sleep(0.04)
        #         leave_town()
        after = image_processing.adventure_image_processing.check_if_hero_is_dead_first()
        GUI_handling.AdventureGUI.end_turn()
        player.day += 1
        execute_detecting_enemy_turn(player.heroes[0])
        for row in advAI.map.obj:
            for tile in row:
                if not isinstance(tile, int):
                    tile.end_day(player)
        if player.day == 8:
            GUI_handling.AdventureGUI.accept_offer()
            # przelec po wszystkim koniec tygodnia

            player.day = 1
            player.week += 1
            for row in advAI.map.obj:
                for tile in row:
                    if not isinstance(tile, int):
                        tile.end_week(player)
            if player.week == 5:
                player.month += 1
                player.week = 1

            # At the end of the week we add all the cities to the adventureAI goals (only if specific castle is not
            # already in the goal list) ---- CamaroTheBOSS
            advAI.addCastlesToGoals()

        # ACTUALIZE HEROES MOVEMENT
        for hero in player.heroes:
            hero.mspoints = movment(hero)
