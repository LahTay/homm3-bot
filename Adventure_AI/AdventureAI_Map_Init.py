"""
This is the script that initializes the map.
Description of the objects on map
0 -> obstacle
1 -> grass
2 -> dirt

THESE THINGS WE DETECT WITH TESSERACT
3 -> random resource
4 -> random dwelling (IT has 2square size (left and right tile))
5 -> random castle
6 -> random monster
7 -> random artifact

8 -> treasure chest
On the map we have hardcoded objects as well (check theRest list in initMap() function)
"""
import copy

import numpy as np
import cv2
from data.creature_banks import Imp_Cache, Dragon_Fly_Hive, Crypt, Cyclops_Stockpile, Dwarven_Treasury, Medusa_Stores
from data.objects_on_map import Sawmill, Ore_Pit, Crystal_Cavern, Gem_Pond, Alchemists_Lab, Sulfur_Dune, Gold_Mine, \
    Fountain_of_Fortune, Redwood_Observatory, Shrine_Of_Magic_Incantation, Mystical_Garden, Temple, \
    Mercenary_Camp, Tree_Of_Knowledge, Rally_Flag, Windmill, Witch_Hut, Arena, Shrine_Of_Magic_Gesture, Water_Wheel, \
    Shrine_Of_Magic_Thought, Marletto_Tower, Magic_Well, Freelancers_Guild, Black_Market, Learning_Stone, \
    Faerie_Ring, Idol_of_Fortune, Den_of_Thieves, Library_of_Enlightenment, School_of_War, Garden_of_Revelation, \
    School_of_Magic, Star_Axis, War_Machine_Factory, Mine
from data.resources import Sulfur, Crystal, Gold, Gems


def initMap():
    """
    Function which initialize our hardcoded, a bit modified "Darwin's Prize" map. It reads .png file which describes
    what is located at specific tile (Red -> Obstacle, Dark brown -> Grass, Brown -> Dirt, Purple -> Resource,
    Green -> Dwelling, Blue -> Monster, Yellow -> Artifact, Cyan -> Treasure Chest). Png has empty spaces at some tiles.
    These tiles are Other Objects (Mines, Buildings, Fountains etc.). Empty spaces are collected to unknown list and
    then are filled with Other Objects from theRest list in specific order.

    :return: modified Darwin's Prize object map (numpy array)
    """
    MAP = np.ones((72, 72), dtype=object) * 9
    img = cv2.imread("map/mapMask.png")
    unknown = []
    for x in range(72):
        for y in range(72):
            pixel = img[x * 32 + 16, y * 32 + 16]
            if pixel[0] == 0 and pixel[1] == 0 and pixel[2] == 255:
                # Obstacle
                MAP[x, y] = 0
            elif pixel[0] == 0 and pixel[1] == 96 and pixel[2] == 140:
                # Grass
                MAP[x, y] = 1
            elif pixel[0] == 69 and pixel[1] == 143 and pixel[2] == 225:
                # Dirt
                MAP[x, y] = 2
            elif pixel[0] == 137 and pixel[1] == 0 and pixel[2] == 140:
                # Resource
                MAP[x, y] = 3
            elif pixel[0] == 10 and pixel[1] == 166 and pixel[2] == 0:
                # Dwelling
                MAP[x, y] = 4
            elif pixel[0] == 166 and pixel[1] == 0 and pixel[2] == 15:
                # Monster
                MAP[x, y] = 6
            elif pixel[0] == 0 and pixel[1] == 251 and pixel[2] == 255:
                # Artifact
                MAP[x, y] = 7
            elif pixel[0] == 244 and pixel[1] == 255 and pixel[2] == 0:
                # Treasure Chest
                MAP[x, y] = 8
            else:
                # If tile at the png mask of the map is empty, there is unknown object yet so we append this position to
                # unknown list
                unknown.append((x, y))

    # The buildings and specific objects
    theRest = [Mystical_Garden, Sawmill, Temple, Mercenary_Camp, Tree_Of_Knowledge,
               5, Mystical_Garden, Rally_Flag, 5, Sulfur_Dune,
               Imp_Cache, Ore_Pit, Windmill, Sulfur, 1, Crystal_Cavern, Windmill,
               Shrine_Of_Magic_Incantation, Redwood_Observatory, Idol_of_Fortune,
               Crystal, War_Machine_Factory, Crystal, Ore_Pit, Shrine_Of_Magic_Incantation,
               Gem_Pond, Sawmill, Witch_Hut, Fountain_of_Fortune, Arena, Gold_Mine,
               Shrine_Of_Magic_Gesture, Gold, Gold, Gold, Gold, School_of_Magic,
               Temple, Redwood_Observatory, Gold, Gold, Water_Wheel, Den_of_Thieves, Temple,
               Water_Wheel, Dragon_Fly_Hive, Crypt, Crystal_Cavern, Shrine_Of_Magic_Thought,
               Sulfur_Dune, Gem_Pond, 0, Crypt, Marletto_Tower, Temple, Gold_Mine,
               Cyclops_Stockpile, Magic_Well, Gold, Gold, Idol_of_Fortune,
               Rally_Flag, Alchemists_Lab, Garden_of_Revelation, Idol_of_Fortune, Idol_of_Fortune,
               Freelancers_Guild, Shrine_Of_Magic_Incantation, Star_Axis, Magic_Well,
               Gem_Pond, Gems, Gems, Shrine_Of_Magic_Gesture, Shrine_Of_Magic_Gesture,
               Rally_Flag, Witch_Hut, Dwarven_Treasury, Alchemists_Lab, Ore_Pit, Black_Market, Redwood_Observatory,
               Ore_Pit, Alchemists_Lab, Crypt, Library_of_Enlightenment, Windmill,
               Mystical_Garden, Redwood_Observatory, Magic_Well, Fountain_of_Fortune, Shrine_Of_Magic_Incantation,
               School_of_War, 5, Temple, Magic_Well, Shrine_Of_Magic_Thought, Temple, Sawmill,
               5, Windmill, Fountain_of_Fortune, Mystical_Garden, Imp_Cache, Mystical_Garden,
               Redwood_Observatory, Ore_Pit, Idol_of_Fortune, Garden_of_Revelation, Idol_of_Fortune,
               0, Windmill, 0, 3, Gold, 3, Shrine_Of_Magic_Incantation, Shrine_Of_Magic_Thought, Fountain_of_Fortune,
               Witch_Hut, Crystal_Cavern, Magic_Well, Rally_Flag, Temple, Crypt, Sawmill,
               5, Learning_Stone, Faerie_Ring, Shrine_Of_Magic_Gesture, Star_Axis,
               Gem_Pond, Medusa_Stores]

    # theRest list has hardcoded objects in specific order (from left upper corner to right down corner) and it contains
    # objects which will be used for filling empty (unknown list) positions on our map, so we iterate through theRest
    # list and just filling the map on the unknown positions with theRest objects.
    for i, item in enumerate(theRest):
        if isinstance(item, Mine):
            mine = copy.deepcopy(item)
            mine.position = (unknown[0][1], unknown[0][0])
            MAP[unknown[0]] = mine
        else:
            MAP[unknown[0]] = item
        del unknown[0]

    return MAP
