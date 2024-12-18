"""Module responsible for image processing in the adventure map department"""
import time
import numpy as np
from mss import mss
import GUI_handling.AdventureGUI
from GUI_handling import AdventureGUI
from data.player_data import Player
from image_processing.CNN_learning import CNN
from image_processing.blue_hero import check_if_blue_hero_exists
from image_processing.screen_slicing import take_console
import cv2, os
from image_processing.ocr import read_generic_text
from difflib import get_close_matches
from image_processing.ocr_dict import *
from image_processing.screen_slicing import ScreenStorage, take_small_map
from skimage.metrics import structural_similarity as ssim


# def initialize_BNN():
#     BNN = CNN((11, 11, 3), "./model/map/", 519)
#     BNN.load_model()
#     return BNN


# def predict_map(map: CNN, screen: ScreenStorage):
#     screen.take_adventure_map()
#     adv_map = map.model.predict(screen.cells, batch_size=1560)
#     adv_map2 = []
#     for i in range(1560):
#         adv_map2.append(int((np.where(adv_map[i] == np.amax(adv_map[i])))[0]))
#     return adv_map2


# def fill_adv_map(cells):
#     cells = np.array(cells)
#     cells = np.array([*map(map_dict.get, cells)])
#     pack = np.ones((30, 52))
#     cells = cells.reshape(30, 52)
#     return cells


# def turn(map: CNN, screen: ScreenStorage):
#     map = predict_map(map, screen)
#     map2 = fill_adv_map(map)
#     return map2h


# def matching_adventure(template_list, screen):
#     smallpoints = np.zeros((52, 30))
#     positions = []
#     max_val_locations = []  # list of tuples indicating where values above a certain threshold are stored.
#     screen.take_battle_templates()
#     for template in template_list:
#         img = screen.screen.copy()
#         method = eval("cv2.TM_CCOEFF_NORMED")
#         res = cv2.matchTemplate(img, template, method)
#         for i in range(52):  # taking only points that are connected to hexes on map
#             for j in range(30):
#                 smallpoints[i, j] = np.amax(res[5 + 32 * j - 5:5 + 32 * j + 5, 5 + 32 * i - 5:5 + 32 * i + 5])
#
#         for i in range(52):  # this is responsible for finding and saving locations of highest values in
#             for j in range(30):  # smallpoints array. Threshold 0.9 is applied.
#                 if smallpoints[i, j] > 0.9:
#                     max_val_locations.append((i, j))
#
#         # I kinda dont know what to do now :/
#         """
#         if max_val > 0.3:  # it should take only real positions and ignore all later units, value needs change and some work on templates to better differentiate real units from terrain
#             top_left = max_loc
#             min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
#             top = max_loc
#             bottom_right = (top[0] + 45, top[1] + 85)
#             cv2.rectangle(screen.screen, top, bottom_right, (100, 100, 100),
#                           -1)  # change to image to eliminate unit which is detected by this match
#             positions.append(top_left)
#             i = i + 1
#         else:
#             i = i + 1
#             positions.append((-1,-1))
#         """
#     return max_val_locations


# def template_adventure(
#         screen: ScreenStorage):  # needs some change for later turns, simple check for minimal value of match instead taking only units before next turn
#
#     templates = []
#     template_list = []
#     for filename in os.listdir(os.path.join("template/")):
#         img = cv2.imread(os.path.join("template/", filename))
#         templates.append(img)
#
#     pos = []
#     # 2 checks for eliminating errors from animating units
#     first = matching_adventure(template_list, screen)
#     time.sleep(0.5)
#     second = matching_adventure(template_list, screen)
#     for i in range(len(first)):
#         if first[i][0] == -1:
#             pos.append(second[i])
#         else:
#             pos.append(first[i])


# bnn = initialize_BNN()
# screen = ScreenStorage()
# time.sleep(5)
# out = turn(bnn,screen)
# print(1)

def detect_thing_ocr(player: Player, position: tuple, type, drillMouse=False):
    """
    function detecting objects with usage of ocr

    :param drillMouse: (bool) makes some mouse shakes before the detection
    :param player: player object
    :param position: position of object
    :param type: type of object we are pointing to
    :return: detected object
    """
    relative_X = position[0] - player.camera[0]
    relative_Y = position[1] - player.camera[1] if type != "Castle" else position[1] - player.camera[1] - 1
    camera_to_position(player, position, relative_X, relative_Y)
    time.sleep(0.08)
    img = take_console()
    if drillMouse:
        time.sleep(0.1)
        GUI_handling.AdventureGUI.move_mouse_by_pixel_relative(32, 0)
        time.sleep(0.1)
        GUI_handling.AdventureGUI.move_mouse_by_pixel_relative(-32, 0)
        time.sleep(0.1)
    text = read_generic_text(img, 2)
    print(f"[OCR INFO]:")
    print(f"    TEXT: {text}")
    print(f"    DETECTION POSITION: {position}")
    print(f"    OBJECT TYPE: {type}")
    print(f"    CAMERA POSITION: {player.camera}")

    if text == "":
        return 1

    if type == "Castle":
        spl = text.partition(", ")
        name = spl[2]
        cityname = spl[0]
        words = towns
        obj = towns_obj
    elif type == "Creature":
        part = text.partition(" of ")
        num2 = part[0]
        num2 = num2.partition(" (")[0]
        temp = get_close_matches(num2, amount, 1)[0]
        num2 = amount_num[amount.index(temp)]
        unit_count = num2
        name = part[2]
        words = creatures
        obj = creatures_obj
    elif type == "Building":
        name = text
        words = habitats
        obj = habitats_obj
        x = position[0]
        y = position[1]
    elif type == "Resource":
        name = text
        words = resource
        obj = resource_obj
    elif type == "Artifact":
        name = text
        words = artifacts
        obj = artifacts_obj
    result = get_close_matches(name, words, 1)
    try:
        num = words.index(result[0])
    except:
        num = 0
    if type == "Creature":
        unit = obj[num]
        out = Slot(unit, unit_count)
    elif type == "Castle":
        unit = deepcopy(obj[num])
        out = unit
        out.name = name
        out.position = position
        out.name_of_city = cityname
    elif type == "Building":
        unit = deepcopy(obj[num])
        out = unit
        out.x = x
        out.y = y
    else:
        unit = deepcopy(obj[num])
        out = unit
    return out


def distance(point, points):
    """
    function checking distance between point and kist of points

    :param point: checked point
    :param points: list of points with labels
    :return: name of nearest element of points to point
    """
    dst = []
    for x in points:
        y = x[0]
        dst.append(((point[0] - y[0]) ** 2) + ((point[1] - y[1]) ** 2) + ((point[2] - y[2]) ** 2))
    dst = np.array(dst)
    dst = np.sqrt(dst)
    result = np.where(dst == np.amin(dst))
    i = dst[int(result[0])]
    if i < 30:
        return points[int(result[0])][1]
    else:
        return "none"


def find_heroes(screen: ScreenStorage, objMap):
    """
    function finding all visible heroes

    :param screen: screen slicing object
    :return: list of all heroes on map
    """
    AdventureGUI.move_mouse_and_click_adventure(1810, 245)
    time.sleep(0.3)
    images = take_small_map()
    tmp = []
    for y in range(72):
        for x in range(72):
            if objMap[x, y] != 0:
                color = distance(images[y][x], screen.colors_small_map)
                if color != "none":
                    tmp.append((x, y, color))
    time.sleep(0.04)
    AdventureGUI.leave_screen()
    time.sleep(0.04)
    screen.hero_positions = tmp
    print(f"[FOUND HEROES]:")
    for h in tmp:
        print(f"    {h}")
    return tmp


# simpledt method to check if someone owns a mine
def check_mine_owner_ocr(player: Player, position: tuple):
    """
    function checking owner of select mine

    :param player: player object
    :param position: position of mine
    :return: color of owner
    """
    relative_X = position[0] - player.camera[0]
    relative_Y = position[1] - player.camera[1]
    camera_to_position(player, position, relative_X, relative_Y)
    time.sleep(0.04)
    img = take_console()
    text = read_generic_text(img, 2)
    spl = text.split()
    owner = spl[-3]
    out = get_close_matches(owner, ["Red", "Blue", "Orange", "Green", "Teal", "Tan", "Purple", "Pink"], 1)
    return out


# minor changes from base function so why not
# def check_hero_name_ocr(player: Player, position: tuple):
#     relative_X = position[0] - player.camera[0]
#     relative_Y = position[1] - player.camera[1]
#     camera_to_position(player, position, relative_X, relative_Y)
#     time.sleep(0.04)
#     img = take_console()
#     text = read_generic_text(img, 2)
#     spl = text.split()
#     name = spl[len(spl) - 1]
#     return name


def camera_to_position(player: Player, position: tuple, relative_X, relative_Y):
    """
    function moving mouse over select coordinates

    :param player: player object
    :param position: chosen point
    :param relative_X: distance between chosen point and camera
    :param relative_Y: distance between chosen point and camera
    """
    if relative_X > 25 or relative_X < -25 or relative_Y > 14 or relative_Y < -14:
        print(f"[CAMERA] {relative_X, relative_Y}")
        # move to nearest hero/city
        dist = np.hypot(relative_X, relative_Y)
        hero = False
        town = False
        n = 0
        for i, x in enumerate(player.heroes):
            temp = np.hypot(x.position[0], x.position[1])
            if temp < dist:
                hero = True
                dist = temp
                n = i
        for i, x in enumerate(player.cities):
            temp = np.hypot(x.position[0], x.position[1])
            if temp < dist:
                town = True
                dist = temp
                n = i
        if town:
            AdventureGUI.press_town(n)
            player.camera = player.cities[n].position
        elif hero:
            AdventureGUI.press_hero(n)
            player.camera = player.heroes[n].position
        relative_X = position[0] - player.camera[0]
        relative_Y = position[1] - player.camera[1]
        # moving camera to position near detected element
        if relative_X > 25 or relative_X < -25 or relative_Y > 14 or relative_Y < -14:
            camerax = player.camera[0]
            cameray = player.camera[1]
            if relative_Y > 0:
                while relative_Y > 10:
                    AdventureGUI.move_camera_down()
                    relative_Y -= 3
                    cameray -= 3
                    time.sleep(0.04)
            else:
                while relative_Y < -10:
                    AdventureGUI.move_camera_up()
                    relative_Y += 3
                    cameray += 3
                    time.sleep(0.04)
            if relative_X > 0:
                while relative_X > 25:
                    AdventureGUI.move_camera_left()
                    relative_X -= 3
                    camerax -= 3
                    time.sleep(0.04)
            else:
                while relative_X < -25:
                    AdventureGUI.move_camera_right()
                    relative_X += 3
                    camerax += 3
                    time.sleep(0.04)
            player.camera = (camerax, cameray)
    AdventureGUI.move_mouse_to_tile_adventure(relative_X, relative_Y)


def detect_hero_move(player, screen, objMap):
    """
    function checking movement of our hero

    :param player: player object
    :param screen: screenslicing object
    :return: pair of tuples containing move of hero
    """
    old_list = deepcopy(screen.hero_positions)
    new_list = find_heroes(screen, objMap)
    pos_new = []
    pos = []
    for y in old_list:
        if y[2] == player.color:
            tmp = (y[0], y[1])
            pos.append(tmp)
    for y in new_list:
        if y[2] == player.color:
            tmp = (y[0], y[1])
            pos_new.append(tmp)
    old = list(set(pos) - set(pos_new))
    new = list(set(pos_new) - set(pos))

    # If new has more elements than 1, that means some of these are fake and we need to test which one -- CamaroTheBOSS
    if len(new) > 1:
        coordinates = new.copy()
        for coord in coordinates:
            ifHero, heroName = check_if_blue_hero_exists(player, coord)
            if not ifHero:
                new.remove(coord)

    return old, new


def remove_dead_heroes(player: Player):
    """
    function for removing dead heroes from our herolist

    :param player: player object
    """
    return False
    list_of_all_heroes = []
    list_of_current_heroes = []
    for i, x in enumerate(player.heroes):
        time.sleep(0.04)
        GUI_handling.AdventureGUI.move_mouse_over_hero(i)
        time.sleep(0.1)
        list_of_all_heroes.append(x.name)
        text = take_console()
        word = read_generic_text(text)
        name = word.partition(" the ")[0]
        text = get_close_matches(name, list_of_all_heroes, 1)
        if len(text) == 0:
            text = ""
        else:
            text = text[0]
        list_of_current_heroes.append(text)
    dead_heroes = []
    for i, x in enumerate(list_of_all_heroes):
        if x in list_of_current_heroes:
            pass
        else:
            dead_heroes.append(i)
    dead_heroes.reverse()
    for x in dead_heroes:
        player.heroes.pop(x)


def check_if_hero_is_dead(player: Player, hero):
    """
    function for removing dead heroes from our herolist

    :param player: player object
    :param hero: hero object
    """
    return False
    list_of_all_heroes = []
    list_of_current_heroes = []
    time.sleep(0.1)
    for i, x in enumerate(player.heroes):
        time.sleep(0.1)
        GUI_handling.AdventureGUI.move_mouse_over_hero(i)
        time.sleep(0.1)
        list_of_all_heroes.append(x.name)
        img = take_console()
        word = read_generic_text(img)
        name = word.partition(" the ")[0]
        text = get_close_matches(name, list_of_all_heroes, 1)
        if len(text)==0:
            text = ""
        else:
            text = text[0]
        list_of_current_heroes.append(text)
    if hero.name in list_of_current_heroes:
        dead = False
        pass
    else:
        player.heroes.remove(hero)
        dead = True
    return dead


def check_if_hero_is_dead_first():
    """
    first part of checking if hero died

    :return: image of list of heroes before move
    """
    with mss() as sct:
        monitor = {'top': 200, 'left': 1740, 'width': 40, 'height': 250}
        screen = np.array(sct.grab(monitor))
        screen = cv2.cvtColor(screen,cv2.COLOR_RGBA2GRAY)
        return screen


def check_if_hero_is_dead_last_without_hero(earlier,player):
    """
    second part of checking if hero died

    :param earlier: output of first function
    :param player: player object
    :return bool indicating if hero has died
    """
    with mss() as sct:
        monitor = {'top': 200, 'left': 1740, 'width': 40, 'height': 250}
        time.sleep(0.2)
        screen = np.array(sct.grab(monitor))
        screen = cv2.cvtColor(screen,cv2.COLOR_RGBA2GRAY)
        score = ssim(earlier,screen)
        if score > 0.9:
            return False
        else:
            return True


def check_if_hero_is_dead_last(earlier,player,hero):
    """
    second part of checking if hero died

    :param earlier: output of first function
    :param player: player object
    :param hero: checked hero
    :return bool indicating if hero has died
    """
    with mss() as sct:
        monitor = {'top': 200, 'left': 1740, 'width': 40, 'height': 250}
        time.sleep(0.2)
        screen = np.array(sct.grab(monitor))
        screen = cv2.cvtColor(screen,cv2.COLOR_RGBA2GRAY)
        score = ssim(earlier,screen)
        if score > 0.9:
            return False
        else:
            player.heroes.remove(hero)
            return True


def remove_lost_cities(player: Player):
    """
    function for removing lost cities from our citylist

    :param player: player object
    """
    list_of_all_cities = []
    list_of_current_cities = []
    for i, x in enumerate(player.cities):
        GUI_handling.AdventureGUI.move_mouse_over_town(i)
        time.sleep(0.04)
        list_of_all_cities.append(x.name_of_city)
        text = take_console()
        word = read_generic_text(text)
        name = word.partition(", ")[0]
        print(f"NAME: {name}")
        print(f"LIST OF ALL CITIES: {list_of_all_cities}")
        text = get_close_matches(name, list_of_all_cities, 1)[0]
        list_of_current_cities.append(text)
    lost_cities = []
    for i, x in enumerate(list_of_all_cities):
        if x in list_of_current_cities:
            pass
        else:
            lost_cities.append(i)
    lost_cities.reverse()
    for x in lost_cities:
        player.cities.pop(x)
