import os

import battleAI.reward as rw
import battleAI.reinforcmentLearningTest as rLT
import data.classes_const as cc
import numpy as np

from keras import Sequential
from keras.layers import Dense, Flatten, Input, Conv2D, MaxPooling2D, Dropout
from tensorflow.keras.optimizers import Adam
from data.BattleAI_environment_needs import Obstacle

import time
import random

if __name__ == "__main__":
    os.chdir("../")


def policy(gameState, deepQAgent, possibleMoves):
    """
    Function choosing action of creature

    :param gameState:   4D array - current state of our environment
    :param deepQAgent:  current agent
    :param possibleMoves:   2D array specifying on which tiles unit can or can't move
    :return:    chosen tile coordinates, chosen action index, indexes of possible actions,actions probabilities
    """
    statesNum = deepQAgent.actionsNum
    rng = np.random.uniform()
    # epsilon = deepQAgent.epsilon
    epsilon = 0                    # epsilon set to 0 when not training
    # flatten possible moves
    possibleIdxs = []
    for coords in np.argwhere(possibleMoves != 0):
        possibleIdxs.append(int(coords[0] + coords[1] * 15))
    # with probability = epsilon choose random action
    if rng < epsilon:
        actValues = np.random.random(statesNum[0])
        maxPossibleActVal = np.max(actValues[possibleIdxs])
        actIDX = np.argwhere(actValues == maxPossibleActVal)[0][0]
        if deepQAgent.bufferCounter < deepQAgent.batch_size:
            pass
        elif deepQAgent.epsilon > deepQAgent.min_epsilon:
            deepQAgent.epsilon *= .99
        else:
            deepQAgent.epsilon = deepQAgent.min_epsilon
    # with probability = 1 - epsilon choose action based on agents model
    else:
        gameState = gameState.reshape((-1,) + gameState.shape)
        actValues = deepQAgent.mod.predict(gameState, verbose=0)[0]
        maxPossibleActVal = np.max(actValues[possibleIdxs])
        actIDX = np.argwhere(actValues == maxPossibleActVal)
        actIDX = [idx for idx in actIDX if idx in possibleIdxs]
        actIDX = actIDX[0][0]

    # convert action to coordinates of a hex tile
    actX = actIDX % 15
    actY = actIDX // 15
    moveAction = (actX, actY)
    actionsProbabilities = -1000000 * np.ones_like(actValues)
    actionsProbabilities[possibleIdxs] = actValues[possibleIdxs]

    # returns action, action values
    return moveAction, int(actIDX), possibleIdxs, actionsProbabilities


def createTeams(creaturesList):
    """
    Creates random teams

    :param creaturesList: list of instances of class Creature
    :return: list of instances of class CreatureBox
    """
    creatures = []
    # randomly choose number of stacks for each player
    playerN = np.random.randint(1, 9)
    opponentN = np.random.randint(1, 9)
    # randomly choose initial positions of stacks
    posOpponent = random.sample(range(0, 11), opponentN)
    posPlayer = random.sample(range(0, 11), playerN)

    for idx in range(playerN):
        # randomly choose creature type
        typeIdx = np.random.randint(0, len(creaturesList))
        unitType = creaturesList[typeIdx]
        # randomly choose quantity of creatures in a stack
        quantity = np.random.randint(0, 50)
        creatures.append(rLT.CreatureBox(unitType, (unitType.size - 1, posPlayer[idx]), quantity))
    for idx in range(opponentN):
        # randomly choose creature type
        typeIdx = np.random.randint(0, len(creaturesList))
        unitType = creaturesList[typeIdx]
        # randomly choose quantity of creatures in a stack
        quantity = np.random.randint(0, 50)
        creatures.append(rLT.CreatureBox(unitType, (15 - unitType.size, posOpponent[idx]), quantity, allied=False))
    return creatures


def createObstacle():
    """
    Creates random obstacles

    :return: list of instances of class Obstacle
    """
    obstacles = []

    obstacleN = np.random.randint(0, 10)
    point = random.sample([[x, y] for x in range(2, 13) for y in range(11)], obstacleN)
    for idx in range(obstacleN):
        o = Obstacle(tuple(point[idx]))
        obstacles.append(o)
    return obstacles


def resetEnv(creatures, obstacles):
    """
    Reset environment

    :param creatures: list of instances of class CreatureBox
    :param obstacles: list of instances of class Obstacle
    :return:
    """
    environment = rLT.Environment(creatures, obstacles)
    return environment


class DQNAgent:

    def __init__(self, name, buffer_size=60000, batch_size=64, start_epsilon=.99, min_epsilon=.2):
        """
        Deep Q learning agent class

        :param name: str - name of the agent
        :param buffer_size: int - size of the buffer in which we remember states, rewards and such
        :param batch_size:  int - size of a batch on which we train the agent each time
        :param start_epsilon:   float - starting possibility of agent choosing random action
        :param min_epsilon: float - minimum value to which possibility of agent choosing random action can decrease
        """
        self.name = name
        self.buffer_size = buffer_size
        self.batch_size = batch_size
        self.bufferCounter = 0

        self.inputShape = (15, 11, 6)
        self.actionsNum = (165,)
        self.states = np.zeros(((self.buffer_size,) + self.inputShape))
        self.actions = np.zeros(self.buffer_size, dtype=int)
        self.terminal_states = np.ones(self.buffer_size, dtype=int)

        self.discount = .99
        self.rewards = np.zeros((self.buffer_size, 1))
        self.nextStates = np.zeros(((self.buffer_size,) + self.inputShape))
        self.possibleMovesBuffer = np.zeros(((self.buffer_size,) + self.actionsNum))

        self.epsilon = start_epsilon
        self.min_epsilon = min_epsilon

        self.mod = self.createModel()
        self.target = self.createModel()

        self.target.set_weights(self.mod.get_weights())

    def save(self, observation):
        """
        Saves current move information to a buffer

        :param observation: list - [state, action, reward, nextState, possible moves, bool: is state terminal?]
        :return:
        """
        if self.bufferCounter >= self.buffer_size:
            self.bufferCounter = self.buffer_size
            self.states = np.delete(self.states, 0)
            self.actions = np.delete(self.actions, 0)
            self.rewards = np.delete(self.rewards, 0)
            self.nextStates = np.delete(self.nextStates, 0)
            self.possibleMovesBuffer = np.delete(self.possibleMovesBuffer, 0, axis=0)
            self.terminal_states = np.delete(self.terminal_states, 0)

        idx = self.bufferCounter
        self.states[idx] = observation[0]
        self.actions[idx] = observation[1]
        self.rewards[idx] = observation[2]
        self.nextStates[idx] = observation[3]
        self.possibleMovesBuffer[idx][:] = 0
        self.possibleMovesBuffer[idx][observation[4]] = 1
        self.terminal_states[idx] = int(not observation[5])

        self.bufferCounter += 1

    def createModel(self):
        """
        creates the neural network model

        :return: neural network model
        """
        model = Sequential()

        model.add(Input(shape=self.inputShape))

        model.add(Flatten())

        model.add(Dense(64))
        model.add(Dense(128))
        model.add(Dense(256))
        model.add(Dense(512))
        model.add(Dense(1024))
        model.add(Dense(2048))
        model.add(Dense(1024))
        model.add(Dense(512))
        model.add(Dense(256))
        model.add(Dense(self.actionsNum[0], activation='linear'))
        model.compile(optimizer=Adam(learning_rate=0.001), loss='mse', metrics=['accuracy'])
        model.summary()
        return model

    # update the agent
    def update(self, stateBatch, actionBatch, rewardBatch, nextStateBatch, possibleIdxsBatch, terminal_statesBatch):
        """
        updates the agent

        :param stateBatch: list - batch of states
        :param actionBatch: list - batch of actions
        :param rewardBatch: list - batch of rewards
        :param nextStateBatch: list - batch of next states
        :param possibleIdxsBatch: list - batch of possible moves
        :param terminal_statesBatch: list - batch of information whether the state is terminal
        """
        # get predicted Q values
        predictedQs = self.mod.predict(stateBatch, verbose=0)
        targetQs = np.copy(predictedQs)
        # get next Q values
        nextQs = self.target.predict(nextStateBatch, verbose=0)

        batchIdx = np.arange(self.batch_size, dtype=np.int32)
        # get target Q values:
        targetQs[batchIdx, actionBatch] = rewardBatch.reshape(-1) + terminal_statesBatch*self.discount * np.max(nextQs, axis=1)


        targetQs[possibleIdxsBatch == 0] = 0

        # train the model
        self.mod.fit(stateBatch, targetQs, batch_size=self.batch_size, epochs=1, verbose=1)

    def learn(self):
        """
        samples random batch of transitions and calls the update method of the agent
        """
        if self.bufferCounter < self.batch_size:
            return
        batchIndxes = np.random.choice(min(self.buffer_size,self.bufferCounter), self.batch_size)

        stateBatch = self.states[batchIndxes]
        actionBatch = self.actions[batchIndxes]
        rewardBatch = self.rewards[batchIndxes]
        nextStateBatch = self.nextStates[batchIndxes]
        possibleIdxsBatch = self.possibleMovesBuffer[batchIndxes]
        terminal_statesBatch = self.terminal_states[batchIndxes]

        self.update(stateBatch, actionBatch, rewardBatch, nextStateBatch, possibleIdxsBatch, terminal_statesBatch)


def saveBuffer(deepQAgent, path):
    """
    Saves the buffer to numpy files

    :param deepQAgent: DQNAgent class instance
    :param path: path to which the files should be saved
    """
    np.save(path + deepQAgent.name + "_states.npy", deepQAgent.states)
    np.save(path + deepQAgent.name + "_actions.npy", deepQAgent.actions)
    np.save(path + deepQAgent.name + "_rewards.npy", deepQAgent.rewards)
    np.save(path + deepQAgent.name + "_nextStates.npy", deepQAgent.nextStates)
    np.save(path + deepQAgent.name + "_buffercounter.npy", np.array([min(deepQAgent.bufferCounter, deepQAgent.buffer_size)]))
    print(f"save: {deepQAgent.name}")


def loadBuffer(deepQAgent, path):
    """
    Loads the buffer from the numpy files if they exist

    :param deepQAgent: DQNAgent class instance
    :param path: path from which the files should be loaded
    """
    try:
        deepQAgent.states = np.load(path + deepQAgent.name + "_states.npy")
        deepQAgent.actions = np.load(path + deepQAgent.name + "_actions.npy")
        deepQAgent.rewards = np.load(path + deepQAgent.name + "_rewards.npy")
        deepQAgent.nextStates = np.load(path + deepQAgent.name + "_nextStates.npy")

        deepQAgent.bufferCounter = np.load(path + deepQAgent.name + "_buffercounter.npy")[0]
        print(f"load: {deepQAgent.name}")
    except:
        print("Error while loading files")


def saveWeights(deepQAgent, path):
    """
    Saves the weights of the agent

    :param deepQAgent: DQNAgent class instance
    :param path: path to which the weights should be saved
    """
    deepQAgent.mod.save_weights(path + deepQAgent.name + "_weights.h5")
    print(f"save weight: {deepQAgent.name}")


def loadWeights(deepQAgent, path):
    """
    Loads the weights of the agent if they exist

    :param deepQAgent: DQNAgent class instance
    :param path: path from which the weights should be loaded
    """
    try:
        deepQAgent.mod.save_weights(path + deepQAgent.name + "_weights.h5")

        deepQAgent.target.set_weights(deepQAgent.mod.get_weights())
        print(f"load weight: {deepQAgent.name}")
    except:
        print("Error while loading files")


def learningProccess():
    """
    Starts the learning process of our agents
    """
    playerAgent = DQNAgent("player", buffer_size=100000, start_epsilon=.8, min_epsilon=.2)
    opponentAgent = DQNAgent("opponent", buffer_size=100000, start_epsilon=.8, min_epsilon=.2)

    folderPath = "./battleAI/battleModel"
    loadBuffer(playerAgent, folderPath)
    loadBuffer(opponentAgent, folderPath)

    loadWeights(playerAgent, folderPath)
    loadWeights(opponentAgent, folderPath)

    creaturesList = [getattr(cc, item) for item in dir(cc) if isinstance(getattr(cc, item), cc.Creature)]
    env = rLT.Environment(createTeams(creaturesList), [])

    tmp = 0
    checkpointVal = 200
    stepAlly = 0
    stepEnemy = 0
    rew = 0

    printInfo = False
    # main loop
    while True:
        print("NEW EPISODE--------------------------------------------------------------------------------------")
        c = createTeams(creaturesList)
        o = createObstacle()
        env = resetEnv(c, o)
        reward = rw.Reward(env)

        currUnit = env.queue.queue[-1]  # get current unit from queue
        # get state and prepare it to feed it into neural network
        state = env.prepareInputForNN(currUnit.field)
        reward.done = False

        while not reward.done:
            if printInfo:
                if rew != 0: env.printEnvironment()
            currUnit = env.queue.queue[-1]  # get current unit from queue
            _, posibleMoves = rLT.Environment.choosePossibleMoves(env, currUnit)
            prevHP = reward.getTeamHP(currUnit, False)
            reward.saveUnitHealth(currUnit)
            # choose agent according to unit side
            if currUnit.ally:
                agent = playerAgent
                stepAlly += 1
                step = stepAlly
            else:
                agent = opponentAgent
                stepEnemy += 1
                step = stepEnemy

            # get action based on policy
            action, actIdx, possibleIdxs, possibilities = policy(state, agent, posibleMoves)
            if printInfo: print("Current position: ", currUnit.field, "Destination: ", action)
            # perform an action
            env.moveCreature(action)
            # get next state
            newState = env.prepareInputForNN(currUnit.field)
            # calculate reward
            rew, battle_result = reward.calcReward(currUnit, env)
            if printInfo: print("Estimated reward: ", rew)

            # save transition into agents memory
            agent.save((state, actIdx, rew, newState, possibleIdxs, reward.done))

            # update state
            state = newState
            time.sleep(tmp)
            # update model
            agent.learn()

            if step % 100:
                agent.target.set_weights(agent.mod.get_weights())
            if step % checkpointVal == 0:
                saveBuffer(agent, folderPath)
                saveWeights(agent, folderPath)

            step += step


if __name__ == "__main__":
    learningProccess()
