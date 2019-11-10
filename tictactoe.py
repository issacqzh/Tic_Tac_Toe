import sys
import numpy as np
import random

# Transition function: P(s, a, s'), specifies
# probability of arriving at any state s' after
# performing action a in state s.

# Reward function: R(s, a), specifies reward AI
# receives after performing action a in state s.
# AI wins = 1, AI loses = -1, Tie = 0.

# Assumptions: 4x4x4 board, line of 4 wins
dim = 4
cube = (4, 4, 4)

# Player X marks cell as 1.
# Player O marks cell as -1.
players = [1, -1]

# All cells initialized to 0.
def initializeState():
    return np.zeros(cube).astype("int")

def initializeVals():
    return np.zeros(cube).astype("double")

def printState(state):
    print(state)

def getEmptySlots(state):
    empty_slots = []

    for i in range(dim):
        for j in range(dim):
            for k in range(dim):
                if state[i][j][k] != 1 and state[i][j][k] != -1:  # empty slot
                    empty_slots.append((i, j, k))
    return empty_slots

# Make a designated move
def playMove(state, player, i, j, k):
    empty_slots = getEmptySlots(state)
    if (i, j, k) in empty_slots:
        state[i][j][k] = player
    else:
        print("Error: Slot (" + str(i) + "," + str(j) + "," + str(k) + ") is occupied.")

# Make a random move
def randomMove(state, player):
    slot = random.choice(getEmptySlots(state))
    state[slot[0]][slot[1]][slot[2]] = player

# If all slots are filled -> tie.
def isTie(state):
    for i in range(dim):
        for j in range(dim):
            for k in range(dim):
                if state[i][j][k] != 1 and state[i][j][k] != -1:  # empty slot
                    return False
    return True

# Returns player 1, player -1, 0 for no winner (as of now), 2 for tie.
def currWinner(state):

    if isTie(state):
        return 2

    for plane in state:

        print("Col sums: " + str(np.sum(np.array(plane), axis=0)))
        print("Row sums: " + str(np.sum(np.array(plane), axis=1)))

        # Checks all cols in plane
        if any(np.sum(np.array(plane), axis=0) == 4):
            return 1
        elif any(np.sum(np.array(plane), axis=0) == -4):
            return -1

        # Checks all rows in plane
        if any(np.sum(np.array(plane), axis=1) == 4):
            return 1
        elif any(np.sum(np.array(plane), axis=1) == -4):
            return -1

        # Checks major diagonals (top left to bottom right) in plane
        major_sum = np.sum(np.diagonal(np.array(plane)))
        print("Horizontal plane maj diagonal: " + str(major_sum))
        if major_sum == 4:
            return 1
        elif major_sum == -4:
            return -1

        # Checks minor diagonal (top right to bottom left) in plane
        minor_sum = np.sum(np.diagonal(np.fliplr(np.array(plane))))
        print("Horizontal plane min diagonal: " + str(minor_sum))
        if minor_sum == 4:
            return 1
        elif minor_sum == -4:
            return -1

    # Checks cross layer diagonals &
    # diagonals running along left to right
    # planes of cube
    lr_plane_major_sum = np.sum(np.diagonal(np.array(state)))
    lr_plane_minor_sum = np.sum(np.diagonal(np.fliplr(np.array(state))))

    print("LR plane maj diagonal: " + str(lr_plane_major_sum))
    print("LR plane min diagonal: " + str(lr_plane_minor_sum))

    if lr_plane_major_sum == 4:
        return 1
    elif lr_plane_major_sum == -4:
        return -1

    if lr_plane_minor_sum == 4:
        return 1
    elif lr_plane_minor_sum == -4:
        return -1

    # Checks cross layer diagonals running along
    # front to back planes of cube
    temp = np.rot90(state, axes=(1, 2))
    fb_plane_major_sum = np.sum(np.diagonal(np.array(temp)))
    fb_plane_minor_sum = np.sum(np.diagonal(np.fliplr(np.array(temp))))

    print("FB plane maj diagonal: " + str(fb_plane_major_sum))
    print("FB plane min diagonal: " + str(fb_plane_minor_sum))

    if fb_plane_major_sum == 4:
        return 1
    elif fb_plane_major_sum == -4:
        return -1

    if fb_plane_minor_sum == 4:
        return 1
    elif fb_plane_minor_sum == -4:
        return -1

    # Checks cross layer columns
    cross_layer_col_sum = 0
    for i in range(dim):
        for j in range(dim):
            for plane in state:
                cross_layer_col_sum += plane[i][j]
                if cross_layer_col_sum == 4:
                    return 1
                elif cross_layer_col_sum == -4:
                    return -1
            cross_layer_col_sum = 0

    return 0

def duplicateState(state):
    new_state = np.zeros(cube).astype("int")
    for i in range(dim):
        for j in range(dim):
            for k in range(dim):
                new_state[i][j][k] = state[i][j][k]
    return new_state

# Program starts here...
# Games played by AI vs AI
state_vals_AI_1 = initializeVals()
state_vals_AI_2 = initializeVals()

if len(sys.argv) == 4:
    n1 = sys.argv[1]
    n2 = sys.argv[2]
    n3 = sys.argv[3]
else:
    n1 = 100
    n2 = 500
    n3 = 2000

# Explore with probability epsilon
# Exploit with probability 1 - epsilon
# Decrease epsilon over time until it approaches 0
epsilon = 0.3

# Discount factor that makes AI place a greater value on
# immediate rewards.
gamma = 0.9


# TODO: Testing
startingState = initializeState()
# printState(startingState)
playMove(startingState, players[1], 0, 1, 1)
playMove(startingState, players[1], 0, 2, 2)
playMove(startingState, players[1], 0, 3, 3)
playMove(startingState, players[1], 0, 0, 0)
# print(currWinner(startingState))
print("----------------")
# print(startingState)

