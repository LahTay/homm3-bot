"""
This module is responsible for decision making of our agent on the adventure map.
"""
import numpy as np

import image_processing.adventure_image_processing
from Adventure_AI.AdventureAI_Map_Init import initMap
from GUI_handling.AdventureGUI import center_on_hero, move_to_tile_adventure, next_hero, move_camera_right, \
    move_camera_left, move_camera_up, move_camera_down
from data.Artifacts import Artifact
from data.creature_banks import Creature_Bank
from data.habitats_on_map import Habitat_On_Map
from data.hero import Slot
from data.objects_on_map import Treasure_Chest, DissapearOnClick, LuckMorale, ObjectOnMap, Mine
from data.resources import Resource
from image_processing.adventure_image_processing import detect_thing_ocr, find_heroes, detect_hero_move
from image_processing.screen_slicing import ScreenStorage
from data.player_data import Player
from time import sleep

# Hierarchy function imports
import hierarchyFunctions.miscFunc as misC
import hierarchyFunctions.artifact_value as artval
import hierarchyFunctions.creature_banks_value as bankval
import hierarchyFunctions.enter_city_value as cityval
import hierarchyFunctions.explorationBoost as fowVal
import hierarchyFunctions.neutral_enemies_value as cval
import hierarchyFunctions.mines_and_resources_value as resourceval
import hierarchyFunctions.habitats_value_evaluation as habitats
import hierarchyFunctions.group_value as group

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

from image_processing.ok_detection import check_ok
from misc.timing import timing


def findPath(other: tuple, node: tuple, matrix: np.ndarray):
    """
    Function which finds path between point A and point B on the specific matrix. Used in costOfThePath() function

    :param other: point A
    :param node: point B
    :param matrix: specific matrix where the path will be found
    :return: cost of the path
    """
    # 1. Define grid, start point and endpoint
    grid = Grid(matrix=np.transpose(matrix))
    start = grid.node(other[0], other[1])
    end = grid.node(node[0], node[1])

    # 2. Find a path
    finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
    path, runs = finder.find_path(start, end, grid)
    if len(path) == 0:
        return 1000000

    # 3. Calculate cost of the path
    cost = 0
    for idx in range(len(path) - 1):
        if path[idx][0] != path[idx + 1][0] and path[idx][1] != path[idx + 1][1]:
            cost += 141
        else:
            cost += 100

    return cost


def tileInControlZone(tilePos: tuple, objMatrix: np.ndarray):
    """
    Function which tests whether specific coordinate is located in the interior of the control zone. It investigates
    neighbours of the tested coordinate and looks for Slot class objects (neutral monsters)

    :param tilePos: coordinates of the tested point
    :param objMatrix: matrix which contains information about all the objects on the map
    :return: boolean value about being or not being in control zone
    """
    x1, x2, y1, y2 = takeSquareAroundXYinRange(tilePos)
    for x in range(x1, x2):
        for y in range(y1, y2):
            if isinstance(objMatrix[x, y], Slot):
                if (x, y) != tilePos:
                    return True
    return False


def costOfThePath(start: tuple, goal: tuple, heroesOnMap: list, matrix):
    """
    Function which calculates cost of the path from point A to point B on specific matrix. This function contains
    preparations for using findPath function.

    :param start: point A
    :param goal: point B
    :param heroesOnMap: list with all the heroes on the map (we need to treat them like an obstacle)
    :param matrix: specific matrix where path will be found
    :return cost: integer value which is movement cost a hero need to bear to get to the goal point
    """
    # Border cases
    if start == goal:
        return 0
    elif tileInControlZone(goal, matrix.obj):
        return 3000000
    # TODO temporary solution for fountains (we need to visit it from the specific side (bottom side))
    elif isinstance(matrix.obj[goal], LuckMorale):
        if matrix.obj[goal].name == "Fountain_of_Fortune":
            return 40000

    # 1. Remember original values of the matrix in *node* and *other* points
    originalNodeValue = matrix.maskMap[goal]
    originalOtherValue = matrix.maskMap[start]

    # 2. Set positions occupied by heroes to obstacle (on pathfinding matrix)
    for hero in heroesOnMap:
        matrix.maskMap[hero.position] = 0

    # 3. Change values in the matrix in *node* and *other* points to one (we need to can reach these points)
    matrix.maskMap[goal] = 1
    matrix.maskMap[start] = 1

    # 4. If its cost to the monster, delete its control zone
    a = takeSquareAroundXYinRange(goal)
    if isinstance(matrix.obj[goal], Slot):
        matrix.maskMap[a[0]:a[1], a[2]:a[3]] = matrix.controlZones[goal]
        matrix.maskMap[goal] = 1

    # 5. Calculate cost with prepared matrix
    cost = findPath(start, goal, matrix.maskMap)

    # 6. If its cost to the monster, switchback control zone
    if isinstance(matrix.obj[goal], Slot):
        matrix.maskMap[a[0]:a[1], a[2]:a[3]] = 0

    # 7. Turn back heroes position to 1 on maskMap
    for hero in heroesOnMap:
        matrix.maskMap[hero.position] = 1

    # 8. Switchback matrix in *node* and *other* points to their original values
    matrix.maskMap[goal] = originalNodeValue
    matrix.maskMap[start] = originalOtherValue
    return cost


def takeSquareAroundXYinRange(xy, squareRange: int = 1):
    """
    Function which takes square area around specific coordinates in specific range. It returns list=[x1, x2, y1, y2]
    where (x1, y1) is left up corner of the area and (x2, y2) is right down corner of the area. It pays attention to map
    boundaries. Works only for 72x72 arrays.

    :param xy: center of the square area
    :param squareRange: (a - 1)/2 of the square where a is square's side's length.
    :return: list with coordinates where (x1, y1) is left up corner of the area and (x2, y2) is right down corner of the
    area
    """
    x, y = xy
    x1 = 0 if (x - squareRange) < 0 else (x - squareRange)
    x2 = 72 if (x + squareRange) > 72 else (x + squareRange + 1)
    y1 = 0 if (y - squareRange) < 0 else (y - squareRange)
    y2 = 72 if (y + squareRange) > 72 else (y + squareRange + 1)
    return [x1, x2, y1, y2]


def getSquareFromMatrix(squareCoord: list, matrix: np.ndarray):
    """
    Returns numpy array fragment of another numpy array from given left up (x1, y1) and right down (x2, y2) corners of
    the area.

    :param squareCoord: list with coordinates [x1, x2, y1, y2]
    :param matrix: numpy array from which we want to cut some square area
    :return: numpy area which is fragment of the matrix param
    """
    return np.copy(matrix[squareCoord[0]:squareCoord[1], squareCoord[2]:squareCoord[3]])


def calculateFinalValue(itm):
    return itm.val / (itm.cost * 0.5 + 1)


def getNextBestTarget(items: list):
    """
    Function which appoints next best goal from list of goals. The best goal is the goal with biggest difference between
    value of the goal and its path cost.

    :param items: list of goals
    :return: best goal
    """
    itemsCopy = items.copy()
    itemsCopy.sort(key=lambda itm: calculateFinalValue(itm), reverse=True)

    # On the sorted list we are now looking for target with value greater than zero and cost less than 50000
    for goal in itemsCopy:
        if goal.val >= 0 and goal.cost < 50000:
            print("[CHOSEN TARGET]")
            print(f"    COORD: {goal.co_ordinates}")
            print(f"    VALUE: {goal.val}")
            print(f"    COST: {goal.cost}")
            print(f"    FINAL VALUE: {round(calculateFinalValue(goal), 5)}")
            return goal

    print("[NO TARGET CHOSEN]")
    return 0


class Item(object):
    def __init__(self, coord, val, cost):
        """
        Dataclass of the goal. It has information about coordinates of the goal, its value and cost to it

        :param coord:
        :param val:
        :param cost:
        """
        self.co_ordinates = coord
        self.val = val
        self.temp_val = 0
        self.cost = cost

    def getValue(self):
        """
        Returns value of the Item (goal)

        :return value:
        """
        return self.val

    def __hash__(self):
        return hash(self.co_ordinates)

    def __eq__(self, other):
        return self.co_ordinates == other.co_ordinates

    def __ne__(self, other):
        return not (self == other)


class MapData:
    def __init__(self):
        """
        MapData is a class where the information about objects, discovered tiles, pathfinding mask (maskMap) and
        control zones of the creatures are stored
        """
        # Init objMap with all the objects at the map (habitats, castles, monsters, free spaces like grass and dirt)
        # and init fowMap with all the discovered tiles (1 means tile is discovered, 0 means it is under fow of war)
        # heroesMap contains information about positions of the heroes at the whole map
        self.obj = np.transpose(initMap())
        self.fog = np.zeros_like(self.obj)
        self.heroes = np.zeros_like(self.obj)
        self.items = []

        # Create maskMap for A* algorithm
        self.maskMap = np.zeros_like(self.obj)
        self.controlZones = {}  # We need to pay attention to control zone of the neutral monsters
        for x in range(72):
            for y in range(72):
                if self.obj[x, y] == 1 or self.obj[x, y] == 2:
                    self.maskMap[x, y] = 1

                # Init control zone of the monster
                elif self.obj[x, y] == 6:
                    self.controlZones[(x, y)] = np.ndarray([])

        self.fillControlZones()

    def fillControlZones(self):
        """
        Function which fills initialized control zones of the monsters at the map. We need to remember state of the
        control zones for pathfinding algorithm. Control zone is like obstacle at the maskMap (map for pathfinding),
        but is changing in remembered state when we are moving to the neutral creature which is owner of this control
        zone.
        """
        # Remember area without control zone and put control zone to maskMap array
        # We will be deleting control zone always when calculating cost to the neutral mob and always when we beat
        # the monster
        for monsterPosKey in self.controlZones.keys():
            # Returns list with two points: left up corner and right down corner
            a = takeSquareAroundXYinRange(monsterPosKey)

            # Returns area of a matrix with given left up and right down corners list
            area = getSquareFromMatrix(a, self.maskMap)

            # Remember this area and set maskMap for this range to zeros
            self.controlZones[monsterPosKey] = area
            self.maskMap[a[0]:a[1], a[2]:a[3]] = 0


class AdventureAI:
    def __init__(self, playerClass: Player):
        """
        AdventureAI class is responsible for moving hero on adventure map, choosing goals and doing actions like
        collecting resources etc.

        :param playerClass: player object
        """
        next_hero()
        # Utility needs for the adventure AI
        self.screen = ScreenStorage()
        self.player = playerClass

        # Creating map instance
        self.map = MapData()

        # Here we dynamically store graph with information about possible targets to choose by the heroes
        self.goals = []

        # Heroes list contains allied Hero instances, heroPointer is used for handling currentHero who we choose in
        # game at the right part of the game window
        self.heroes = self.player.heroes
        self.heroPointer = None

        # We need to remember enemy coordinates, because we need to actualize their position in goals
        self.enemyCoordinates = []

        self.initStartHeroPosition()

    def initStartHeroPosition(self):
        """
        Function which initializing start position of the hero at the start of the game
        """
        # 1. Find hero starting position
        next_hero()
        heroes = find_heroes(self.screen, self.map.obj)

        # 2. Set this position to the hero and actualize camera position
        x, y, color = heroes[0]
        self.heroes[0].position = (x, y)
        self.map.heroes[x, y] = color
        self.heroPointer = 0
        self.player.camera = (x, y)

        # 3. Discover our initial city, append it to goals and actualize obj map
        castle = detect_thing_ocr(self.player, (x, y), "Castle")
        self.player.cities.append(castle)
        self.map.obj[x, y] = castle

        # 4. Discover the rest of the area around the hero initial position
        self.discoverAreaAroundXY(self.currHero().position)

    def cameraOnCurrentHero(self):
        """
        Function which centers camera to the current hero
        """
        if self.player.camera != self.currHero().position:
            self.player.camera = self.currHero().position
            center_on_hero()

    def discoverAreaAroundXY(self, xy: tuple):
        """
        Function which discovers circular area around specific coord at the map

        :param xy: center of discovered area
        """
        x, y = xy
        # # 2.1 Define variables which create area to discover (square from (x1, y1) to (x2, y2) + small areas around
        # # this square)
        x1 = x - 5
        x2 = x + 6
        y1 = y - 5
        y2 = y + 6
        if x1 < 0:
            x1 = 0
            mx1 = 5 - x
        else:
            mx1 = 0
        if x2 > 72:
            x2 = 72
            mx2 = 66 - x
        else:
            mx2 = 11
        if y1 < 0:
            y1 = 0
            my1 = 5 - y
        else:
            my1 = 0
        if y > 72:
            y2 = 72
            my2 = 66 - y
        else:
            my2 = 11

        # Mask defines shape of the discovered area
        mask = np.transpose(np.asarray(([0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
                                        [0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                                        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                                        [0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                                        [0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0])))
        mask = mask[mx1:mx2, my1:my2]
        for cx in range(x1, x2):
            for cy in range(y1, y2):
                # Check only tiles from mask (it defines shape of the discovered area)
                if mask[cx - x1, cy - y1]:
                    if not self.map.fog[cx, cy]:
                        self.map.fog[cx, cy] = 1
                        self.detectXY((cx, cy))

        # checking the borders and eventually adding goals
        self.discoveryValue(x, y, x1, False, False, True, False)
        self.discoveryValue(x, y, x2, False, False, False, True)
        self.discoveryValue(x, y, y1, True, False, False, False)
        self.discoveryValue(x, y, y2, False, True, False, False)

    def detectXY(self, target: tuple):
        """
        Function which are detecting specific tile on the map. Using OCR

        :param target: (coordinates of tile)
        """
        # Only int type objects we need to detect with tesseract
        # (check AdventureAI_Map_Init for more info)
        if isinstance(self.map.obj[target], int):
            if self.map.obj[target] == 4:
                self.detectDwelling(target)
            else:
                self.detectAnotherObjects(target)
        elif not isinstance(self.map.obj[target], Habitat_On_Map):
            self.goals.append(Item(target, 0, 0))

    def detectDwelling(self, target):
        """
        Detection function for random dwellings. Used in detectXY function.

        :param target: (coordinates of tile)
        """
        # 1. Detect dwelling type and test if we are detecting left or right side of the building
        x, y = target
        thing = detect_thing_ocr(self.player, (x, y), "Building")

        # 2. Determining whether detected part of the building is left
        # Boundary cases
        if x == 71:
            part = "right"
        elif x == 0:
            part = "left"
        # Usual cases
        elif self.map.obj[x + 1, y] == 4:
            part = "left"
        else:
            part = "right"

        # If we detected left side of the building
        if part == "left":
            # If entrance is on the left side we can add this building to goals
            if thing.entrance == "left":
                self.map.obj[x, y] = thing
                self.map.obj[x + 1, y] = 0
                self.goals.append(Item((x, y), 0, 0))
            # Otherwise (entrance is on the right side) we need to check whether right side of the building is
            # discovered. If is not, we cannot add this building to goals
            elif self.map.fog[x + 1, y]:
                self.map.obj[x, y] = 0
                self.map.obj[x + 1, y] = thing
                self.goals.append(Item((x + 1, y), 0, 0))

        # If we detected right side of the building
        else:
            # If entrance is on the right side we can add this building to goals
            if thing.entrance == "right":
                self.map.obj[x, y] = thing
                self.map.obj[x - 1, y] = 0
                self.goals.append(Item((x, y), 0, 0))
            # Otherwise (entrance is on the left side) we need to check whether left side of the building is
            # discovered. If is not, we cannot add this building to goals
            elif self.map.fog[x - 1, y]:
                self.map.obj[x - 1, y] = thing
                self.map.obj[x, y] = 0
                self.goals.append(Item((x - 1, y), 0, 0))

    def detectAnotherObjects(self, target):
        """
        Detection function for all random things which are not random dwellings. Used in detectXY function.

        :param target: (coordinates of tile)
        """
        # 0, 1, 2 are undetectable (obstacles and empty spaces)
        if 0 <= self.map.obj[target] <= 2:
            return 0

        # 8 on map is equal to Treasure Chest
        if self.map.obj[target] == 8:
            self.map.obj[target] = Treasure_Chest
            self.goals.append(Item(target, 0, 0))
            return 0

        # 1. Detect what is it with OCR
        argDictionary = {3: "Resource", 5: "Castle", 6: "Creature", 7: "Artifact"}
        thing = detect_thing_ocr(self.player, target, argDictionary[self.map.obj[target]])

        # 2. Add detected thing to goals
        self.map.obj[target] = thing
        self.goals.append(Item(target, 0, 0))

    def discoveryValue(self, x, y, x1, top, bottom, left, right):
        """
        Function which adds exploration goals to the list with goals

        :param x:
        :param y:
        :param x1:
        :param top:
        :param bottom:
        :param left:
        :param right:
        :return:
        """
        # check borders for exploring
        # discovery goal value
        discoveryBonus = 50
        undiscovered = False

        # depending on the border to be checked the variables change
        border = xvar1 = xvar2 = yvar1 = yvar2 = 0
        if left:
            border, xvar1, xvar2, yvar1, yvar2 = -1, -5, -3, -2, 3
        if right:
            border, xvar1, xvar2, yvar1, yvar2 = 1, 4, 6, -2, 3
        if top:
            border, xvar1, xvar2, yvar1, yvar2 = -1, -2, 3, -5, -3
        if bottom:
            border, xvar1, xvar2, yvar1, yvar2 = 1, -2, 3, 4, 6

        # gotta make sure to not get out of range
        if 0 <= (x1 + border) < 72:
            # we check whether there is undiscovered area around hero
            if left or right:
                for yl in range(y - 2, y + 3):
                    if not self.map.fog[x1 + border, yl]:
                        undiscovered = True
            else:
                for xl in range(x - 2, x + 3):
                    if not self.map.fog[xl, x1 + border]:
                        undiscovered = True
            if undiscovered:
                # first we check whether we have any goals near the border that we are checking
                for xl in range(x + xvar1, x + xvar2):
                    for yl in range(y + yvar1, y + yvar2):
                        # if we have a goal there, we will go there eventually so no need to add anything
                        if Item((xl, yl), 0, 0) in self.goals:
                            return 0
                # if we got here, it means we have no goals near fogged area
                for xl in range(x + xvar1, x + xvar2):
                    for yl in range(y + yvar1, y + yvar2):
                        # check whether we can walk there
                        if self.map.obj[xl, yl] == 1 or self.map.obj[xl, yl] == 2:
                            # add a new goal to discover the area
                            self.goals.append(Item((xl, yl), 0, 0))
                            coord = (xl, yl)
                            print(f"[DISCOVERY TARGET] {coord}")
                            return discoveryBonus, coord
        return 0

    def currHero(self):
        """
        Function which get current hero

        :return Hero which is pointed by heroPointer:
        """
        return self.heroes[self.heroPointer]

    def moveCurrentHero(self, target: tuple):
        """
        Function which moves current hero to specific target. It testing whether we are already at the destination
        tile or not and clicks on map to move on specific tile

        :param target: coordinates of specific tile
        :return 0 if we are already on specific tile and we do not need to move, else None:
        """
        # 1. Making move in game if we are not at target tile
        cx, cy = self.currHero().position  # We need target relative to hero position for GUI_handling correct work
        x, y = target
        if (cx, cy) == (x, y):
            self.deleteGoal(target)
            return False
        elif abs(cx - x) >= 25 or abs(cy - y) >= 14:
            self.moveCameraToTarget(target)

        camX, camY = self.player.camera
        move_to_tile_adventure(x - camX, y - camY)

        # 2. Wait for end of the move animation, then discover area around this target tile
        sleep(0.7)
        return True

    def assignValueToTile(self, node: tuple):
        """
        Function which returns value of specific tile at the map. Value is used for choosing best target to visit

        :param node: coordinates of tile
        :return value: value assigned to this tile
        """
        hero = self.currHero()
        obj = self.map.obj[node]
        # If hero is not our main hero and the target is Slot make this target invaluable
        if hero.herotype != "main" and (isinstance(obj, Slot) or isinstance(obj, Creature_Bank)):
            return -1


        value = 0
        value += misC.mp(node, hero)
        value += misC.disappear_on_click(obj, hero, self.player)
        value += misC.increase_skills(obj, hero)
        value += misC.luck_morale(obj, hero)
        value += misC.the_rest(obj, hero)

        if isinstance(obj, Artifact):
            value += artval.artifact_value(obj, hero)

        if isinstance(obj, Creature_Bank):
            value += bankval.creature_bank_value(obj, hero)

        value += cityval.enter_city_evaluation(obj, self.player, hero)

        value += fowVal.evaluateExplorationBoost(node, self.map)

        value += cval.neutral_enemies_value(hero, obj)

        value += resourceval.mineCase(obj, self.player)
        value += resourceval.resourceStackCase(obj, self.player, hero)

        if isinstance(obj, Habitat_On_Map):
            value += habitats.habitat_on_map_value(obj, hero, self.player)

        return value

    def assign_temp_value_group(self, node):
        """
        Assigns temporal value to tiles, it needs to be temporal because if it was straight up added it would
        artificially increase the value of the tiles surrounding it

        :param node: coordinates of the tile being checked
        :return: temporal value
        """
        hero = self.currHero()
        value = group.group_value(node, hero.value_map)
        return value

    def actualizeCurrHeroPosXDXDXDXDXDXD(self):
        """
        This function find heroes positions at the map and actualize their positions

        :return: (x, y), position of the hero
        """
        # Actualize position of camera and currentHero
        # heroes = find_heroes(self.screen)

        # Bug fix to always find our hero (currently works only for one hero)
        # while not heroes:
        #     next_hero()
        #     heroes = find_heroes(self.screen)

        old, new = detect_hero_move(self.player, self.screen, self.map.obj)
        try:
            print(f"[HERO MOVE] {old[0], new[0]}")
        except:
            pass
        if not len(new) == 0:
            self.currHero().position = new[0]
            self.player.camera = new[0]
            return new[0]

    def actualizeCurrHeroPos(self):
        # Actualize position of camera and currentHero
        heroes = find_heroes(self.screen, self.map.obj)

        # Bug fix to always find our hero (currently works only for one hero)
        while not heroes:
            next_hero()
            heroes = find_heroes(self.screen, self.map.obj)

        x, y = None, None
        for x, y, color in heroes:
            if color == "Red":
                if self.map.obj[x, y] != 0:
                    self.currHero().position = (x, y)
                    self.player.camera = (x, y)

        return x, y

    def playHeroDay(self):
        """
        Function which play one turn for current hero. It does multiple moves till hero has no movement points
        """
        hero = self.currHero()
        print(f"[CURRENT HERO] ------------------------------------------------------------------------")
        print(f"    NAME: {hero.name}")
        print(f"    POSITION: {hero.position}")
        print(f"    MS POINTS: {hero.mspoints}")
        death = False
        # 1. At the start of the day we are adding detected enemies to goals
        if self.heroPointer == 0:
            self.addEnemiesToGoals()

        # 2. Executing whole hero day
        while hero.mspoints > 0 and not death:
            earlier = image_processing.adventure_image_processing.check_if_hero_is_dead_first()
            self.nextMove()
            death = image_processing.adventure_image_processing.check_if_hero_is_dead_last(earlier, self.player, hero)

        # 3. After moving last hero we are deleting detected enemies from goals
        if self.heroPointer == len(self.heroes) - 1:
            self.delEnemiesFromGoals()

    def addEnemiesToGoals(self):
        """
        Function which adds enemy heroes position to the list with goals.
        """
        for enemyHero in self.player.enemies:
            goal = Item(enemyHero.position, 0, 0)
            self.enemyCoordinates.append(goal.co_ordinates)
            self.goals.append(goal)

    def addLostMineToGoals(self, mine: Mine):
        mineGoal = Item(mine.position, 0, 0)
        # Checking whether mine is currently in our goals
        for goal in self.goals:
            if goal.co_ordinates == mine.position:
                return 0
        # If is not in our goals, add it to goals
        self.goals.append(mineGoal)

    def delEnemiesFromGoals(self):
        """
        Function which deletes enemy heroes position from the list with goals.
        """
        allTheGoals = self.goals.copy()
        for goal in allTheGoals:
            if goal.co_ordinates in self.enemyCoordinates:
                self.goals.remove(goal)

    def checkNotResourceDestinationSuccess(self, target: tuple):
        """
        Not resource case for testing if hero have got to the given target or not

        :param target: coordinates of the tile
        """
        okay = check_ok()
        if not okay:
            sleep(1)
            okay = check_ok()
        print(f"OKAY VALUE: {okay}")

        if okay:
            # Do action assigned to the object
            self.map.obj[target].action(self.player, self.currHero(), okay)

            # We achieved the goal so delete it from goals
            self.deleteGoal(target)

            if isinstance(self.map.obj[target], DissapearOnClick) or \
                    isinstance(self.map.obj[target], Slot):
                # Actualize mask map if goal is disappear on click object
                self.actualizeMaskMap(target)

    def checkResourceDestinationSuccess(self, target: tuple):
        """
        Resource case for testing if hero have got to the given target or not

        :param target: coordinates of the tile
        """
        self.actualizeCurrHeroPosXDXDXDXDXDXD()
        thing = detect_thing_ocr(self.player, target, "Resource", drillMouse=True)
        sleep(0.1)
        if not isinstance(thing, Resource):
            # Do action assigned to the object
            self.map.obj[target].action(self.player, self.currHero())
            print(f'    RESOURCES TAKEN')

            # We achieved the goal so delete it from goals
            self.deleteGoal(target)

            # Actualize mask map
            self.actualizeMaskMap(target)

    def checkEmptyDestinationSuccess(self, target: tuple):
        """
        Empty space (exploration goals) case for tmesting if hero have got to the given target or not

        :param target: coordinates of the tile
        """
        heroPos = self.actualizeCurrHeroPosXDXDXDXDXDXD()
        if target == heroPos:
            # We achieved the goal so delete it from goals
            self.deleteGoal(target)
        print(f"[EMPTY DESTINATION CHECK]:")
        print(f"    HERO POS: {heroPos}")
        print(f"    TARGET POS: {target}")

    def actualizeMaskMap(self, target: tuple):
        """
        If we pick up the resource we need to actualize mask map (for pathfinding), this function do it

        :param target: coordinates of the tile
        """
        if isinstance(self.map.obj[target], Resource) or isinstance(self.map.obj[target], DissapearOnClick):
            self.map.obj[target] = 1
            self.map.maskMap[target] = 1
        elif isinstance(self.map.obj[target], Slot):
            a = takeSquareAroundXYinRange(target)
            self.map.maskMap[a[0]:a[1], a[2]:a[3]] = self.map.controlZones[target]
            self.map.obj[target] = 1
            self.map.maskMap[target] = 1

    def nextMove(self):
        """
        Function which move current hero to the best target
        """
        hero = self.currHero()

        # 1 Firstly we need to actualize values of the nodes in targets graph
        self.actualizeValueAndCostsToGoals()

        # 2. Then we get best possible target
        target = getNextBestTarget(self.goals)
        # If target == 0 we do not have any good target to choose so we do nothing :)
        if isinstance(target, int):
            hero.mspoints = -1
            return 0
        self.printTarget(target)

        # 3. Move current hero
        moved = self.moveCurrentHero(target.co_ordinates)
        if not moved:
            return 0

        # 3.1 Checking destination success, if success do action
        if isinstance(self.map.obj[target.co_ordinates], Resource):
            self.checkResourceDestinationSuccess(target.co_ordinates)
            sleep(1)
        elif not isinstance(self.map.obj[target.co_ordinates], int):
            self.checkNotResourceDestinationSuccess(target.co_ordinates)
            sleep(1)
            self.actualizeCurrHeroPosXDXDXDXDXDXD()
        else:
            self.checkEmptyDestinationSuccess(target.co_ordinates)
            sleep(1)

        # 4. Actualize hero movement points and discover area around the him
        hero.mspoints -= target.cost
        self.discoverAreaAroundXY(hero.position)

    def deleteGoal(self, target: tuple):
        """
        Function which deletes specific target. It is called only when we have got to the specific goal

        :param target: coordinates of the tile
        """
        for idx, goal in enumerate(self.goals):
            if target == goal.co_ordinates:
                del self.goals[idx]
                break

    def actualizeValueAndCostsToGoals(self):
        """
        Function which actualize value of goals and costs to these goals. Called always before calling nextMove()
        """
        heroPos = self.currHero().position
        for goal in self.goals:
            goal.cost = costOfThePath(heroPos, goal.co_ordinates, self.player.heroes, self.map)
            goal.val = self.assignValueToTile(goal.co_ordinates)
            self.currHero().value_map[goal.co_ordinates] = goal.val
        for goal in self.goals:
            goal.temp_val = self.assign_temp_value_group(goal.co_ordinates)
            self.currHero().temp_value_map[goal.co_ordinates] = goal.temp_val

        for goal in self.goals:
            goal.val += goal.temp_val
        self.currHero().value_map += self.currHero().temp_value_map

        print("[TARGETS]")
        for t in self.goals:
            thing = "Discovery target"
            if not isinstance(self.map.obj[t.co_ordinates], int):
                if isinstance(self.map.obj[t.co_ordinates], Slot):
                    thing = self.map.obj[t.co_ordinates].unit.name
                else:
                    thing = self.map.obj[t.co_ordinates].name
            print(f"    {t.co_ordinates, t.val, t.cost, calculateFinalValue(t), thing}")

    def printTarget(self, target: Item):
        """
        Function for printing hero's next target in the console. Used for debugging

        :param target: coordinates of the tile
        """
        thing = "Empty space"
        if not isinstance(self.map.obj[target.co_ordinates], int):
            if isinstance(self.map.obj[target.co_ordinates], Slot):
                thing = self.map.obj[target.co_ordinates].unit.name
            else:
                thing = self.map.obj[target.co_ordinates].name
        print("[MOVE FROM A TO B]")
        print(f"    HERO POSITION: {self.currHero().position}")
        print(f"    HERO MOVEMENT POINTS: {self.currHero().mspoints}")
        print(f"    TARGET: {target.co_ordinates} -> {thing}")

    def addCastlesToGoals(self):
        for castle in self.player.cities:
            # Add each castle to the goals only if specific castle is not already in goals
            alreadyInGoals = False
            for goal in self.goals:
                if goal.co_ordinates == castle.position:
                    alreadyInGoals = True
                    break
            if not alreadyInGoals:
                castleGoal = Item(castle.position, 0, 0)
                self.goals.append(castleGoal)

    def moveCameraToTarget(self, target: tuple):
        sleep(0.2)
        tx, ty = target
        cx, cy = self.player.camera
        print("[CAMERA MOVE]")
        print(f"    FROM: {cx, cy}")
        print(f"    DESTINATION: {tx, ty}")
        while abs(cx - tx) > 3 or abs(cy - ty) > 3:
            if cx - tx > 3:
                move_camera_left()
                cx -= 3
            elif cx - tx < -3:
                move_camera_right()
                cx += 3
            elif cy - ty > 3:
                move_camera_up()
                cy -= 3
            elif cy - ty < -3:
                move_camera_down()
                cy += 3
            sleep(0.05)
        self.player.camera = (cx, cy)
