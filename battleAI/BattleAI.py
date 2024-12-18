import cv2
from mss import mss
from battleAI.reinforcmentLearningTest import Environment, divideIntoAllyAndEnemy
from data.BattleAI_environment_needs import *
from image_processing.battle_image_processing import mouse_unit_check, check_terrain, initialize_BNN, initialize_QNN, \
    ScreenStorage, checkIfTurnIsOurs, checkForObstacle
from battleAI.deepQlearning import DQNAgent, policy
from GUI_handling.BattleGUI import *
import numpy as np
import random as rd
import time
import mouse
import keyboard as kb
import os
import copy
from data.hero_specialities import specialities
from data.casting_spells import Use_magic

if __name__ == "__main__":
    os.chdir('../')
# This class is helpful in connecting creatures detected by neural network with creatures in queue
class CreatureMove:
    def __init__(self, detectedMob: CreatureBox):

        self.detectedInstance = detectedMob
        self.fromQueueInstance = None
        self.candidates = []  # list with queue indexes of candidates

    def findCandidates(self, queue):
        for i, mob in enumerate(reversed(queue)):
            if mob.ally:
                break
            if mob.type.name == self.detectedInstance.type.name:
                self.candidates.append(len(queue) - i - 1)


def fitted(mobs: list):
    for mob in mobs:
        if len(mob.candidates) != 1:
            return False
    return True


def take_whole_queue():
    """
    Takes screenshot of the entire queue

    :return: np.array - screenshot of the entire queue
    """
    monitor = {'top': 779, 'left': 662, 'width': 15*40, 'height': 38}
    screen = np.array(mss().grab(monitor))
    return screen


def bookAvailable():
    """
    Checks if we can use the spell or not

    :return: bool - True if available, False otherwise
    """
    book_available = 85     # mean value of spell book icon when it's possible to use it
    book_used = 57          # mean value of spell book icon when it's not possible to use it

    monitor = {'top': 780, 'left': 1311, 'width': 46, 'height': 37}
    screen = np.array(mss().grab(monitor))
    screen = cv2.cvtColor(screen, cv2.COLOR_RGBA2BGR)
    mean = np.mean(screen)

    if abs(mean - book_available) < abs(mean - book_used):
        return True
    else:
        return False


def arePicturesTheSame(pictureA, pictureB):
    """
    Checks if pictures are exactly the same

    :param pictureA: np.array - image
    :param pictureB: np.array - image
    :return: bool - are pictures the same
    """
    return not(np.bitwise_xor(pictureA, pictureB).any())


def arePicturesSimilar(pictureA, pictureB, percent):
    """
    Checks if pictures are similar

    :param pictureA: np.array - image
    :param pictureB: np.array - image
    :param percent: float - acceptable percent of difference between pictures
    :return: bool - are pictures similiar
    """
    truthTable = pictureA == pictureB
    truthTable = truthTable.reshape(-1)

    difference = len(truthTable[truthTable==False])/len(truthTable)
    if difference < percent/100:
        return True
    else:
        return False


def take_side_window():
    """
    Takes screenshot of the side window that pops up when we hover over enemy

    :return: np.array - screenshot of the side window
    """
    monitor = {'top': 492, 'left': 1366, 'width': 1441 - 1366, 'height': 777 - 492}
    screen = np.array(mss().grab(monitor))
    img = cv2.cvtColor(screen, cv2.COLOR_RGBA2BGR)
    return img


def checkIfStillAlive(target, state):
    """
    function checking if our environment is correctly assuming that enemy is still alive
    If not we remove the enemy from environment
    the 2nd output of this function is indicator whether or not the enviroment was changed
    informing us if we should pick action once again

    :param target: tuple - position of checked tile
    :param state: 2D array of objects - current state of our environment
    :return: 2D array of objects - state of our environment, bool - is the target dead
    """
    state = copy.deepcopy(state)
    # if unit decides to defend the target is None
    if target is not None:
        (x, y) = target
    else:
        return state, False
    # if target tile is a creature we move cursor to the top left corner and capture element of the screen
    # where enemy unit info appears after hovering a cursor over it. This will be our referecial image.
    # Next we hover a mouse over the target tile and take shot of the same area on screen as before.
    # Then we compare the 2 images. If they are the same then the tile doesn't contain creature so we need
    # to update our environment else the creature is still there no need to update anything.
    if isinstance(state[x, y], CreatureBox) and not state[x, y].ally:
        mouse.move(0, 0, duration=0)
        time.sleep(0.1)
        reference = take_side_window()
        move_mouse_to_tile(x, y)
        time.sleep(0.1)
        checked = take_side_window()

        # unit already dead
        if arePicturesSimilar(reference, checked, 6):
            state[x, y] = 0
            print("removed dead enemy from ", (x, y))
            return state, True
        else:
            return state, False
    else:
        return state, False


def debunkObstacles(current_position, state, obstacles, hex_img):
    """
    Function removing false positives from detected obstacles
    It works by moving mouse to current unit and pressing ctrl
    to display it's possible moves as dark hexagrams
    this allows us to make good threshold to get the tiles we can really move on
    if our env assumes one of this tiles is an obstacles we correct that mistake

    :param current_position: tuple - current position of our unit
    :param state: 2D array of objects - current state of our environment
    :param obstacles: list of instances of class Obstacle
    :param hex_img: np.array - mask used in checking the possible moves
    :return: state: 2D array of objects - current state of our environment,
             obstacles: list of instances of class Obstacle
    """
    move_mouse_to_tile(current_position[0], current_position[1])
    kb.press('ctrl')
    time.sleep(0.2)
    monitor = {'top': 306, 'left': 618, 'width': 1300 - 618, 'height': 775 - 306}
    img = np.array(mss().grab(monitor))
    kb.release('ctrl')
    img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
    image = cv2.inRange(img, (0, 0, 0), (28, 28, 28))
    eroded = cv2.morphologyEx(image, cv2.MORPH_OPEN, (5, 5), iterations=4)

# pixel coords for the upper left corner of first tile in even row
    even_x = 23
    even_y = 10
# pixel coords for the upper left corner of first tile in odd row
    odd_x = 1
    odd_y = 10
# size of tile's bounding box
    w = 35
    h = 43
# amount of pixels to move when moving to the next row
    dy = 42

    for y in range(11):
        for x in range(15):
            # choosing coordinates depending on the row number parity
            if y % 2 != 0:
                Y = odd_y + dy * y
                X = odd_x + (h + 1) * x
            else:
                Y = even_y + dy * y
                X = even_x + (h + 1) * x
            # checked window (fragment of the picture)
            field = eroded[Y:Y + w, X:X + h]
            # drawing window (for debugging)
            im = eroded.copy()
            bb = cv2.rectangle(im, (X, Y), (X + h, Y + w), (255, 0, 0), 2)
            # number of white pixels in window
            field = np.bitwise_and(hex_img, field)
            whites = np.argwhere(field != 0)
            if len(whites) > 140:
                if isinstance(state[x, y], Obstacle):
                    print("removed ", (x, y))
                    state[x, y] = 0
                    obstacles = [i for i in obstacles if
                                          i.field != (x, y)]
    return state, obstacles


# Checks if the battle has ended by detecting if "ok" button has appeared
def checkIfEnd(ok_button_img):
    """
    Checks if the battle has ended

    :param ok_button_img: np.array - image of ok button to look for
    :return: boot - has the battle ended
    """
    monitor = {'top': 765, 'left': 1109, 'width': 1176 - 1109, 'height': 798 - 765}
    img = np.array(mss().grab(monitor))
    img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)

    if arePicturesTheSame(ok_button_img, img):
        return True
    else:
        return False


def getInitialAmmoDict(units):
    """
    Creates dictionary of units ammunition to keep track of it

    :param units: list of instances of class CreatureBox
    :return: dictionary of units ammunition
    """
    ammo_dict = {}
    for unit in units:
        if unit.type.ammo > 0 and unit.ally:
            ammo_dict.update({unit.field: unit.type.ammo})
    return ammo_dict


def colorDistance(checked, reference):
    """
    Calculates the distance in color space between two colors

    :param checked: 3 element list - checked color
    :param reference: 3 element list - reference color
    :return: distance in color space between two colors
    """
    return np.sqrt((checked[0] - reference[0])**2 + (checked[1] - reference[1])**2 + (checked[2] - reference[2])**2)


def checkTerrainType():
    """
    Checks whether the terrain we are fighting on is Grass or Dirt

    :return: str - terrain we are fighting on
    """
    dirt_terrain_color = [66, 90, 115]
    grass_terrain_color = [24, 90, 82]
    y = 730
    x = 560
    w = 50
    h = 45
    monitor = {'top': y, 'left': x, 'width': w, 'height': h}
    terrain_snippet = np.array(mss().grab(monitor))
    mean_color_value = np.median(terrain_snippet, (0, 1))
    distance1 = colorDistance(mean_color_value, dirt_terrain_color)
    distance2 = colorDistance(mean_color_value, grass_terrain_color)
    if distance1 < distance2:
        return "Dirt"
    else:
        return "Grass"


class BattleAI:

    def __init__(self):
        # 1. Loading battle agent model which will be making decisions
        print(os.getcwd())
        self.agent = DQNAgent("DQNAgent", buffer_size=100, start_epsilon=0, min_epsilon=0)  # load model
        self.agent.mod.load_weights("./battleAI/battleModelplayer_weights.h5")


        # 2. Initialize BattleNeuralNetwork and QueueNeuralNetwork which are processing image data from game and
        # extrude information about game state from it
        self.bnn = initialize_BNN()
        self.qnn = initialize_QNN()
        self.screen = ScreenStorage()
        self.terrain = None
        self.hero_name = None
        self.hero_skills = None
        self.spell_power = None
        self.speed_boosts = {}

        # dictionary keeping track of ranged unit's ammo
        self.ammo_dict = {}
        # array containing hexagram image needed in detecting obstacles
        self.hex_img = np.load(r'./battleAI/hex.npy')

        # 3. Initialize environment
        self.env = None

    def spellEffectInEnv(self, spell_target, spell_name):
        """
        Applies speed effects in our environment

        :param spell_target: tuple - coordinates of the target of our spell
        :param spell_name:  str - name of the spell
        """
        speed_spells = ["Haste", "Prayer"]
        if spell_name not in speed_spells:
            return False

        # Case if spell effects only 1 ally
        for unit in self.env.queue.queue:
            if unit.field in self.speed_boosts.keys():
                prev_boost = self.speed_boosts[unit.field][0]
            else:
                prev_boost = 0
            if spell_name == "Haste":
                if "Air_Magic" in self.hero_skills.keys():
                    if self.hero_skills["Air_Magic"] == 0:
                        if unit.field == spell_target:
                            unit.type.speed += 3 - prev_boost
                            self.speed_boosts.update({unit.field: (3, 0)})
                    elif self.hero_skills["Air_Magic"] == 1:
                        if unit.field == spell_target:
                            unit.type.speed += 5 - prev_boost
                            self.speed_boosts.update({unit.field: (5, 0)})
                    elif self.hero_skills["Air_Magic"] == 1:
                        unit.type.speed += 5 - prev_boost
                        self.speed_boosts.update({unit.field: (5, 0)})
                else:
                    if unit.field == spell_target:
                        unit.type.speed += 3 - prev_boost
                        self.speed_boosts.update({unit.field: (3, 0)})

            elif spell_name == "Prayer":
                if "Water_Magic" in self.hero_skills.keys():
                    if self.hero_skills["Water_Magic"] == 0:
                        if unit.field == spell_target:
                            unit.type.speed += 2 - prev_boost
                            self.speed_boosts.update({unit.field: (2, 0)})
                    elif self.hero_skills["Water_Magic"] == 1:
                        if unit.field == spell_target:
                            unit.type.speed += 4 - prev_boost
                            self.speed_boosts.update({unit.field: (4, 0)})
                    elif self.hero_skills["Water_Magic"] == 2:
                        unit.type.speed += 4 - prev_boost
                        self.speed_boosts.update({unit.field: (4, 0)})
                else:
                    if unit.field == spell_target:
                        unit.type.speed += 2 - prev_boost
                        self.speed_boosts.update({unit.field: (2, 0)})
        return True
    def updateSpdBoosts(self, prev_pos):
        mob = self.env.queue.queue[0]   # unit that just moved

        # if the mob is currently affected by a spell increasing speed
        if prev_pos not in self.speed_boosts.keys():
            return

        # take previous boost info
        prev_boost_info = self.speed_boosts[prev_pos]
        # remove previous boost info from the dict
        self.speed_boosts.pop(prev_pos)
        # if the spell is still active (number of turns it should be active is equal to the spell power of our hero)
        # we increase the number of turns it has been active
        if prev_boost_info[1] + 1 != self.spell_power:
            self.speed_boosts.update({mob.field: (prev_boost_info[0], prev_boost_info[1]+1)})

    def findObstacles(self, units):
        obstaclesList = check_terrain(self.bnn, self.screen, units)
        return obstaclesList

    def findUnits(self):
        unitsList = mouse_unit_check(self.qnn, self.screen)
        uList = copy.deepcopy(unitsList)
        uList = [unit for unit in uList if not isinstance(unit, list)]
        for unit in uList:
            # Add bonus speed for native terrain
            if self.terrain in unit.type.native_terrain:
                unit.type.speed = unit.type.speed + 1
            # Add bonus speed for hero speciality
            if self.hero_name in specialities.keys():
                if unit.type.name in specialities[self.hero_name]:
                    unit.type.speed = unit.type.speed + 1
                elif "Speed" in specialities[self.hero_name]:
                    unit.type.speed = unit.type.speed + 2
            if unit.field in self.speed_boosts.keys():
                unit.type.speed += self.speed_boosts[unit.field][0]
            print(unit.type.name, unit.field, unit.ally, unit.quantity, unit.type.speed)

        return uList

    def start(self, setOfCreatures: list, setOfObstacles: list):
        self.env = Environment(setOfCreatures, setOfObstacles)

    def simulateMoves(self, enemyCreatures: list):
        mobsInOrder = self.__fitDetectedCreaturesToQueueCreatures(enemyCreatures)
        for mob in mobsInOrder:
            self.env.moveCreature(mob.detectedInstance.field)

    def __fitDetectedCreaturesToQueueCreatures(self, enemyCreatures: list):
        # Algorithm
        # 1. Because we have information only about position we need to find all the creatures with the same name and
        # ally from queue. These creatures are candidates for moving
        # 2. We are searching for candidates for every enemy which was moved by opponent
        # 3. Then we are eliminating most distant candidates (further than speed of the creature)
        # 4. Then we look at moving possibilities and we are connecting everything in consistent whole
        # resources        -> mobs we need move to simulate opponent turn in proper order
        # moves            -> target positions we need mobs from resources to move on
        # listOfCandidates -> we need to find connection enemy->resource so listOfCandidates contains candidates for
        #                     these connections

        # 1. Initialise necessary structures and find candidates
        mobs = []
        for enemy in enemyCreatures:
            mob = CreatureMove(enemy)
            mob.findCandidates(self.env.queue.queue)
            mobs.append(mob)

        # 2. FIRST REDUCING PROCESS: Reducing candidates by calculating possible moves and checking if candidate
        # could reach target position
        for mob in mobs:
            if len(mob.candidates) != 1:
                # Iterate through candidates to find who could reach position of detected creature
                candidates = mob.candidates.copy()
                for candidate in candidates:
                    possibleMoves = self.env.choosePossibleMoves(self.env.queue.queue[candidate])  # Get possible moves
                    if not possibleMoves[mob.detectedInstance.field]:
                        mob.candidates.remove(candidate)
        if fitted(mobs):
            mobs.sort(key=lambda x: x.candidates[0], reverse=True)
            return mobs

        # 3. SECOND REDUCE PROCESS Connecting detected creatures who has only one candidate with this candidate and
        # reduce these candidates from other candidates lists
        for mob in mobs:
            if len(mob.candidates) == 1:
                for i in range(len(mobs)):
                    if mob.candidates == mobs[i].candidates:
                        continue
                    elif mob.candidates[0] in mobs[i].candidates:
                        mobs[i].candidates.remove(mob.candidates[0])
        if fitted(mobs):
            mobs.sort(key=lambda x: x.candidates[0], reverse=True)
            return mobs

        # 4. THIRD REDUCE PROCESS We need to resolve some conflicts so firstly we check how many times candidate
        # appear in the candidates list: if candidate appear only once we have to use it in place we found it
        # When counting we can miss lists with length == 1

        # 4.1 Fill counter: two dimensional because we want to remember where we can find this candidate
        counter = np.zeros((len(self.env.queue.queue), 2), dtype=int)
        for i, mob in enumerate(mobs):
            if len(mob.candidates) != 1:
                for candidateIdx in mob.candidates:
                    if counter[candidateIdx][0] == 0:
                        for unit in mobs:
                            if candidateIdx in unit.candidates:
                                counter[candidateIdx][0] += 1
                                counter[candidateIdx][1] = i

        # 4.2 Reduction phase
        for i, pair in enumerate(counter):
            if pair[0] == 1:
                mobs[pair[1]].candidates = [i]

        if fitted(mobs):
            mobs.sort(key=lambda x: x.candidates[0], reverse=True)
            return mobs

        # 5. FOURTH REDUCE PROCESS: last process is resolve conflicts with quantity of the stacks
        # less quantity difference between stacks means that this is real one
        # We will use counter from the previous reduce process. If under index counter is -1 we cant take this candidate
        for mob in mobs:
            if len(mob.candidates) != 1:
                # Calculate differences
                quantityDiffs = np.zeros_like(mob.candidates)
                for i, candidate in enumerate(mob.candidates):
                    quantityDiffs[i] = abs(mob.detectedInstance.quantity - self.env.queue.queue[candidate].quantity)

                # Choose best candidate with minimum quantity difference
                minArg = np.argmin(quantityDiffs)
                bestCandidateIdx = mob.candidates[minArg]

                # If it is accessible take it, if not take something other
                while len(mob.candidates) != 1:
                    if counter[bestCandidateIdx][0] != -1:
                        # If true take it
                        mob.candidates = [bestCandidateIdx]
                        counter[bestCandidateIdx][0] = -1
                    else:
                        # If false remove this from candidate and find for new minimum quantity difference
                        mob.candidates.remove(bestCandidateIdx)
                        quantityDiffs = np.delete(quantityDiffs, minArg)
                        minArg = np.argmin(quantityDiffs)
                        bestCandidateIdx = mob.candidates[minArg]

            else:
                counter[mob.candidates[0]][0] = -1

        mobs.sort(key=lambda x: x.candidates[0], reverse=True)
        return mobs

    def makeMove(self, target: tuple):
        # check if mob is ranged
        ranged_mob = False
        mob = copy.deepcopy(self.env.queue.queue[-1])
        if mob.type.ranged:
            # check number of allies before attacking
            # to determine later if the unit died after a move
            allies, _ = divideIntoAllyAndEnemy(self.env.queue.queue)
            prev_ally_count = len(allies)
            ranged_mob = True
        # 1. Make sure last mob from queue is ours
        # if mob.ally:
        # Move creature in environment
        neighbour = None
        if target is not None:
            target, neighbour = self.env.moveCreature(target)
        else:
            self.env.queue.move()

        # Move creature in game
        if neighbour is None:
            if target is not None:
                move_to_tile(target[0], target[1])
        else:
            attack_enemy(target[0], target[1], neighbour)

        if ranged_mob:
            allies, _ = divideIntoAllyAndEnemy(self.env.queue.queue)
            current_ally_count = len(allies)
            print("Ranged mob")
            if current_ally_count == prev_ally_count:
                print("UPDATED THE DICT")
                # remove previous mob ammo info from dict
                self.ammo_dict.pop(mob.field)
                # add new mob ammo info to dict
                mob = self.env.queue.queue[0]
                self.ammo_dict.update({mob.field: mob.type.ammo})
            # if mob died during moving
            else:
                # remove previous mob ammo info from dict
                self.ammo_dict.pop(mob.field)

    def getAction(self, state):
        """
        Gets action from our agent

        :param state: 3D array - represents current state of our environment
        :return: tuple - chosen tile, current unit, actions probabilities calculated by our agent
        """
        mob = self.env.queue.queue[-1]
        _, possibleMoves = self.env.choosePossibleMoves(mob)
        (x, y), actIDX, possibleIdxs, actionsProbability = policy(state, self.agent, possibleMoves)

        return (x, y), mob, actionsProbability

    def getMoveFromNN(self):
        # 1. Start turn to actualize possibleMoves and prepare input for battle model
        self.env.startTurn()
        state = self.env.prepareInputForNN(self.env.queue.queue[-1].field)

        # 2. Get actions probabilities and take the action with highest probability

        (x, y), mob, actionsProbability = self.getAction(state)
        # 3. If it is not possible to click in the highest probability hex then get another highest probability move
        if not self.checkPossibility((x, y), mob):
            while True:
                if (x, y) == mob.field:
                    actionsProbability[np.argmax(actionsProbability)] = -100000.
                else:
                    actionsProbability[np.argmax(actionsProbability)] = -1000.
                if self.checkPossibility((x, y), mob):
                    break
        self.env.printEnvironment()
        print("After While")

        target = None if (x, y) == mob.field else (x, y)
        if mob.type.size == 2 and (x + 1, y) == mob.field:
            target = None
        print("Choice ", (x, y), "Curr Pos ", mob.field)
        print(mob.field, " move to ", target)
        return target

    def checkPossibility(self, target, mob):
        x, y = target
        if not self.env.possibleMoves[x, y]:  # Basic condition (move has to be reachable)
            print("Not possible")
            return False

        elif (x, y) == mob.field or (mob.type.size == 2 and (x + 1, y) == mob.field):  # Condition for wait/defense execution
            # Wait is problematic, because of the possibility to make one wait per round
            # that's why if this condition is met just defend
            defend()
            print("Defend")
            return True

        else:
            print("Break")
            return True

    def skipEnemiesInQueue(self):
        while not self.env.queue.queue[-1].ally:
            self.env.queue.move()

    def actualizeQueue(self, setOfCreatures: list):
        self.env.queue.queue = []
        for unit in reversed(setOfCreatures):
            # update ammo info
            if unit.field in self.ammo_dict.keys():
                unit.type.ammo = self.ammo_dict[unit.field]
            self.env.queue.queue.append(unit)

    def fight(self, hero_name, skills, spell_power):
        self.hero_skills = skills
        self.hero_name = hero_name
        self.spell_power = spell_power
        ok_button_img = cv2.imread(r'./battleAI/ok_button.png')
        # --- FIRST TURN ---
        while not checkIfTurnIsOurs(self.screen):
            time.sleep(1)

        self.terrain = checkTerrainType()
        # Create new environment, skill all the enemies from queue and do first move
        units = self.findUnits()
        self.ammo_dict = getInitialAmmoDict(units)
        self.start(units, self.findObstacles(units))
        self.env.allowDying = False
        self.skipEnemiesInQueue()
        self.env.printEnvironment()

        # target = self.getMoveFromNN()
        # Use_magic(self.env.queue.queue) # Using spell
        # self.makeMove(target)
        # ------------------
        self.env.printEnvironment()
        time.sleep(3)  # Wait for the end odf the move
        run = True
        changed_speed = False
        # ---- NEXT TURNS ----
        while run:
            # 1. Wait for our turn
            while not checkIfTurnIsOurs(self.screen):
                if checkIfEnd(ok_button_img):
                    run = False
                    move_mouse_and_click_battle(1150, 775)
                    break
                time.sleep(1)

            if not run:
                break

            # 2. When first mob in queue is not friendly we need to actualize environment (synchronize queue and game)
            if not self.env.queue.queue[-1].ally or changed_speed:
                # 2.1 When turn is ours, find units at the battlefield
                units = self.findUnits()

                # 2.2 Actualize environment and queue
                self.env.resetEnv(units, self.env.obstacles)
                self.actualizeQueue(units)
                changed_speed = False

            self.env.printEnvironment()
            if bookAvailable():
                spell_target, spell_name = Use_magic(units)
                changed_speed = self.spellEffectInEnv(spell_target, spell_name)

            # 3. Choose and make move
            while self.env.queue.queue[-1].ally:
                mouse.move(0, 0, duration=0)
                while mouse.get_position() != (0, 0):
                    pass
                time.sleep(1)
                # save queue image before moving
                queue_before = take_whole_queue()

                current_position = self.env.queue.queue[-1].field

                possibleMoves, _ = self.env.choosePossibleMoves(self.env.state[current_position])
                self.env.state, self.env.obstacles = debunkObstacles(current_position, self.env.state, self.env.obstacles, self.hex_img)
                changed = True
                while changed:
                    target = self.getMoveFromNN()
                    self.env.state, changed = checkIfStillAlive(target, self.env.state)
                    if checkIfEnd(ok_button_img):
                        run = False
                        changed = False
                self.makeMove(target)
                self.updateSpdBoosts(current_position)
                time.sleep(3)  # Wait for the end of the move

                # check if the target we just attacked is still alive
                # required in case we got additional turn after killing enemy
                # because in this case the queue will change even though it didn't move
                _, dead = checkIfStillAlive(target, self.env.state)
                # if the target died we need to scan the battle field again
                if dead:
                    break

                # move mouse to the corner just to be sure it's not on queue or creature
                mouse.move(0, 0, duration=0)
                while mouse.get_position() != (0, 0):
                    pass
                time.sleep(1)
                # save queue image after moving
                queue_after = take_whole_queue()
                # if we get additional turn undo moving the queue
                if arePicturesSimilar(queue_before, queue_after, 6):
                    self.env.queue.undoMove()
                elif changed_speed:
                    break
                if checkIfEnd(ok_button_img):
                    run = False
                    move_mouse_and_click_battle(1150, 775)
                    break


if __name__ == "__main__":
    battleAI = BattleAI()
    battleAI.fight("Brissa", {"Air_Magic": 0}, 2)






