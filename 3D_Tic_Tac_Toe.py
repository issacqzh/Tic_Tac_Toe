import random
import pickle
import argparse
import numpy as np

class TicTacToe:
    def __init__(self):
        self.board = [' '] * 64
        self.p1 = None
        self.p2 = None
        self.done = False

    def resetBoard(self):
        self.board = [' '] * 64

    # Helper function
    def printBoard(self):
        print(np.reshape(self.board, (4, 4, 4)))

    def evaluateReward(self, isPlayer1, move):

        # Player tries to overwrite
        if self.board[move] != ' ':
            return -5.0, True

        if isPlayer1:
            mark = 'X'
        else:
            mark = '0'

        # Mark board
        self.board[move] = mark

        # Check each horizontal plane
        for j in range(4):

            offset = j * 16

            # Check rows in plane
            for i in range(4):
                if (self.board[offset + i * 4] == mark and self.board[offset + i * 4 + 1] == mark
                        and self.board[offset + i * 4 + 2] == mark and self.board[offset + i * 4 + 3] == mark):
                    return 1.0, True

            # Check cols in plane
            for i in range(4):
                if (self.board[offset + i + 0] == mark and self.board[offset+i + 4] == mark
                        and self.board[offset + i + 8] == mark and self.board[offset + i + 12] == mark):
                    return 1.0, True

            # Check diagonals in plane
            if (self.board[offset + 0] == mark and self.board[offset + 5] == mark
                    and self.board[offset + 10] == mark and self.board[offset + 15] == mark):
                return 1.0, True

            if (self.board[offset + 3] == mark and self.board[offset + 6] == mark
                    and self.board[offset + 9] == mark and self.board[offset + 12] == mark):
                return 1.0, True

        # Check vertical lines
        for i in range(16):
            if (self.board[i] == mark and self.board[i + 16] == mark
                    and self.board[i + 32] == mark and self.board[i + 48] == mark):
                return 1.0, True

        # Check first row in cube
        for i in range(4):
            if (self.board[i] == mark and self.board[i + 20] == mark
                    and self.board[i + 40] == mark and self.board[i + 60] == mark):
                return 1.0, True

        # Check first col in cube
        for i in range(0, 16, 4):
            if (self.board[i] == mark and self.board[i + 17] == mark
                    and self.board[i + 34] == mark and self.board[i + 51] == mark):
                return 1.0, True

        # Check last row in cube
        for i in range(12, 16):
            if (self.board[i] == mark and self.board[i + 12] == mark
                    and self.board[i + 24] == mark and self.board[i + 36] == mark):
                return 1.0, True

        # Check last col in cube
        for i in range(3, 19, 4):
            if (self.board[i] == mark and self.board[i + 15] == mark
                    and self.board[i + 30] == mark and self.board[i + 45] == mark):
                return 1.0, True

        # Check 4 diagonals in cube
        if (self.board[0] == mark and self.board[21] == mark
                and self.board[42] == mark and self.board[63] == mark):
            return 1.0, True

        if (self.board[3] == mark and self.board[22] == mark
                and self.board[41] == mark and self.board[60] == mark):
            return 1.0, True

        if (self.board[12] == mark and self.board[25] == mark
                and self.board[38] == mark and self.board[51] == mark):
            return 1.0, True

        if (self.board[15] == mark and self.board[26] == mark
                and self.board[37] == mark and self.board[48] == mark):
            return 1.0, True

        # Draw, if all filled slots are filled
        if not any(slot == ' ' for slot in self.board):
            return 0.5, True

        return 0.0, False

    def getPossibleMoves(self):
        return [i for i, mark in enumerate(self.board) if mark == ' ']

    # Begin training
    def startTraining(self, p1, p2, iterations):
        if isinstance(p1, player) and isinstance(p2, player):
            self.p1 = p1
            self.p2 = p2
            self.train(iterations)

    # Training function
    def train(self, iterations):
        for i in range(iterations):
            self.p1.startGame()
            self.p2.startGame()
            self.resetBoard()
            done = False
            isPlayer1 = random.choice([True, False])
            while not done:
                if isPlayer1:
                    move = self.p1.pickMove(self.board, self.getPossibleMoves())
                else:
                    move = self.p2.pickMove(self.board, self.getPossibleMoves())

                reward, done = self.evaluateReward(isPlayer1, move)

                if reward == 1.0:  # Won
                    if isPlayer1:
                        self.p1.updateQVal(reward, self.board, self.getPossibleMoves())
                        self.p2.updateQVal(-1 * reward, self.board, self.getPossibleMoves())
                    else:
                        self.p1.updateQVal(-1 * reward, self.board, self.getPossibleMoves())
                        self.p2.updateQVal(reward, self.board, self.getPossibleMoves())

                elif reward == 0.5:  # Draw
                    self.p1.updateQVal(reward, self.board, self.getPossibleMoves())
                    self.p2.updateQVal(reward, self.board, self.getPossibleMoves())

                elif reward == -5.0:  # Illegal move
                    if isPlayer1:
                        self.p1.updateQVal(reward, self.board, self.getPossibleMoves())
                    else:
                        self.p2.updateQVal(reward, self.board, self.getPossibleMoves())

                elif reward == 0.0:
                    if isPlayer1:
                        self.p1.updateQVal(reward, self.board, self.getPossibleMoves())
                    else:
                        self.p2.updateQVal(reward, self.board, self.getPossibleMoves())

                isPlayer1 = not isPlayer1  # Switch player

    def saveQtables(self, iterations):
        self.p1.saveQtable("./player1Qtable" + str(iterations) + ".txt")
        self.p2.saveQtable("./player2Qtable" + str(iterations) + ".txt")

    def saveQvals(self, iterations):
        self.p1.saveFinalQVals("./player1Qvals" + str(iterations) + ".txt")
        self.p2.saveFinalQVals("./player2Qvals" + str(iterations) + ".txt")

    def printQTables(self, iterations):
        with open("./player1Qtable" + str(iterations) + ".txt", 'rb') as file1:
            print(pickle.load(file1))
        with open("./player2Qtable" + str(iterations) + ".txt", 'rb') as file2:
            print(pickle.load(file2))

    def printQVals(self, iterations):
        with open("./player1Qvals" + str(iterations) + ".txt", 'rb') as file1:
            print(pickle.load(file1))
        with open("./player2Qvals" + str(iterations) + ".txt", 'rb') as file2:
            print(pickle.load(file2))


class player:
    def __init__(self):
        self.epsilon = 0.25
        self.alpha = 0.35
        self.gamma = 0.85
        self.q_table = {}  # Q table
        self.prev_state = None
        self.prev_state_action = None
        self.prev_q = 0.0


    def startGame(self):
        self.prev_state = None
        self.prev_state_action = None
        self.prev_q = 0.0

    # Returns move using a combination of exploration (random) and exploitation (greedy)
    def pickMove(self, state, possible_moves):
        self.prev_state = tuple(state)
        if random.random() < self.epsilon:
            next_move = random.choice(possible_moves)
            self.prev_state_action = (self.prev_state, next_move)
            self.prev_q = self.getQVal(self.prev_state, next_move)
            return next_move
        else:
            q_list = []
            for move in possible_moves:
                q_list.append(self.getQVal(self.prev_state, move))
            max_q = max(q_list)

            # Chooses among them randomly if there's more than 1 best option
            if q_list.count(max_q) > 1:
                best_options = [i for i in range(len(possible_moves)) if q_list[i] == max_q]
                i = random.choice(best_options)
            else:
                i = q_list.index(max_q)

            self.prev_state_action = (self.prev_state, possible_moves[i])
            self.prev_q = self.getQVal(self.prev_state, possible_moves[i])
            return possible_moves[i]

    def getQVal(self, state, action):  # get Q states
        if self.q_table.get((state, action)) is None:
            self.q_table[(state, action)] = 1.0
        return self.q_table.get((state, action))

    def updateQVal(self, reward, state, possible_moves):  # update Q states using Qlearning
        q_list = []
        for moves in possible_moves:
            q_list.append(self.getQVal(tuple(state), moves))

        if q_list:
            max_q_next = max(q_list)
        else:
            max_q_next = 0.0

        max_future_q = (reward + self.gamma * max_q_next) - self.prev_q
        self.q_table[self.prev_state_action] = self.prev_q + self.alpha * (max_future_q)

    def saveQtable(self, filename):
        Qtable = self.getFinalQtable()
        with open(filename, 'wb') as file:
            pickle.dump(Qtable, file)

    # For same states, compare q values and pick the largest one.
    def getFinalQtable(self):
        state_action_value = self.q_table
        temp_Qtable = {}
        for state_action, value in state_action_value.items():
            curr_state = state_action[0]
            try:
                temp_value = temp_Qtable[curr_state]
                if temp_value < value:
                    temp_Qtable[curr_state] = value
            except:
                temp_Qtable[curr_state] = value
        return temp_Qtable

    def saveFinalQVals(self, filename):
        Qvals = self.getFinalQVals()
        with open(filename, 'wb') as file:
            pickle.dump(Qvals, file)

    def getFinalQVals(self):
        state_action_value = self.q_table
        temp_Qtable = {}
        for state_action, value in state_action_value.items():
            curr_state = state_action[0]
            try:
                temp_value = temp_Qtable[curr_state]
                if temp_value < value:
                    temp_Qtable[curr_state] = value
            except:
                temp_Qtable[curr_state] = value
        return list(temp_Qtable.values())


if __name__ == '__main__':
    # CLI format: python 3D_Tic_Tac_Toe.py -n1 100 -n2 500 -n3 2000
    parser = argparse.ArgumentParser(description='num iterations')
    parser.add_argument('-n1', type=int, required=False, default=100, help='smallest num iterations')
    parser.add_argument('-n2', type=int, required=False, default=500, help='medium num iterations')
    parser.add_argument('-n3', type=int, required=False, default=2000, help='largest num iterations')
    args = parser.parse_args()

    game = TicTacToe()  # game instance, True means training
    player1 = player()  # player1 learning agent
    player2 = player()  # player2 learning agent

    print(">>>starting training 1...")
    game.startTraining(player1, player2, args.n1)  # start training
    game.saveQtables(args.n1)
    game.printQTables(args.n1)

    game.saveQvals(args.n1)
    game.printQVals(args.n1)


    print(">>>starting training 2...")
    game.startTraining(player1, player2, args.n2)  # start training
    game.saveQtables(args.n2)
    game.printQTables(args.n2)

    game.saveQvals(args.n2)
    game.printQVals(args.n2)

    print(">>>starting training 3...")
    game.startTraining(player1, player2, args.n3)  # start training
    game.saveQtables(args.n3)
    game.printQTables(args.n3)

    game.saveQvals(args.n3)
    game.printQVals(args.n3)

    # game.printQTables(args.n3)
