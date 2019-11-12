import random
import pickle
import argparse

parser=argparse.ArgumentParser(description='iteration times')
parser.add_argument('--iteration',type=int,default=100, help='number of iterations')
args=parser.parse_args()

class TicTacToe:
    def __init__(self):
        self.board=[' ']*64
        self.done=False
        self.player1=None
        self.player2=None

    def reset(self):
        self.board=[' ']*64

    def evaluate(self,mark):

        # check each horizontal layer
        for j in range(4):
            offset=j*16
            # "rows checking"
            for i in range(4):
                if (self.board[offset+i * 4] == mark and self.board[offset+i * 4 + 1] == mark
                        and self.board[offset+i * 4 + 2] == mark and self.board[offset+i * 4 + 3] == mark):
                    return 1.0, True
            # "col checking"
            for i in range(4):
                if (self.board[offset+i + 0] == mark and self.board[offset+i + 4] == mark
                        and self.board[offset+i + 8] == mark and self.board[offset+i + 12] == mark):
                    return 1.0, True
            # diagonal checking
            if (self.board[offset+0] == mark and self.board[offset+5] == mark
                    and self.board[offset+10] == mark and self.board[offset+15] == mark):
                return 1.0, True

            if (self.board[offset+3] == mark and self.board[offset+6] == mark
                    and self.board[offset+9] == mark and self.board[offset+12] == mark):
                return 1.0, True

        # check each vertical lines
        for i in range(16):
            if (self.board[i] == mark and self.board[i+16] == mark and self.board[i+32] == mark and self.board[i+48] == mark):
                return 1.0, True

        # check first row in 3d
        for i in range(4):
             if (self.board[i] == mark and self.board[i+20] == mark and self.board[i+40] == mark and self.board[i+60] == mark):
                return 1.0, True

        #check first column in dimension
        for i in range(0,16,4):
            if (self.board[i] == mark and self.board[i+17] == mark and self.board[i+34] == mark and self.board[i+51] == mark):
                return 1.0, True
        #check last column in dimension
        for i in range(3,19,4):
            if (self.board[i] == mark and self.board[i+15] == mark and self.board[i+30] == mark and self.board[i+45] == mark):
                return 1.0, True
        #check last row
        for i in range(12,16):
            if (self.board[i] == mark and self.board[i+12] == mark and self.board[i+24] == mark and self.board[i+36] == mark):
                return 1.0, True
        #check 4 diagonal in dimension
        if (self.board[0] == mark and self.board[21] == mark and self.board[42] == mark and self.board[63] == mark):
                return 1.0, True
        if (self.board[3] == mark and self.board[22] == mark and self.board[41] == mark and self.board[60] == mark):
                return 1.0, True
        if (self.board[12] == mark and self.board[25] == mark and self.board[38] == mark and self.board[51] == mark):
                return 1.0, True
        if (self.board[15] == mark and self.board[26] == mark and self.board[37] == mark and self.board[48] == mark):
                return 1.0, True
        # if all filled, then draw
        if not any(slot == ' ' for slot in self.board):
            return 0.5, True
        return 0.0, False

    def possible_moves(self):
        return [moves for moves, v in enumerate(self.board) if v == ' ']

    def step(self, isPlayer1, move):
        if (isPlayer1):
            mark = 'X'
        else:
            mark = '0'
        if (self.board[move] != ' '):  # try to over write
            return -5, True

        self.board[move] = mark
        reward, done = self.evaluate(mark)
        return reward, done

    #begin training
    def startTraining(self,player1,player2):
        if(isinstance(player1,player) and isinstance(player2, player)):
            self.player1=player1
            self.player2=player2

    # training function
    def train(self, iterations):
        for i in range(iterations):
            print("trainining", i)
            self.player1.game_begin()
            self.player2.game_begin()
            self.reset()
            done = False
            isPlayer1 = random.choice([True, False])
            while not done:
                if isPlayer1:
                    move = self.player1.epslion_greedy(self.board, self.possible_moves())
                else:
                    move = self.player2.epslion_greedy(self.board, self.possible_moves())

                reward, done = self.step(isPlayer1, move)

                if reward == 1:  # won
                    if isPlayer1:
                        self.player1.updateQ(reward, self.board, self.possible_moves())
                        self.player2.updateQ(-1 * reward, self.board, self.possible_moves())
                    else:
                        self.player1.updateQ(-1 * reward, self.board, self.possible_moves())
                        self.player2.updateQ(reward, self.board, self.possible_moves())

                elif reward == 0.5:  # draw
                    self.player1.updateQ(reward, self.board, self.possible_moves())
                    self.player2.updateQ(reward, self.board, self.possible_moves())


                elif reward == -5:  # illegal move
                    if isPlayer1:
                        self.player1.updateQ(reward, self.board, self.possible_moves())
                    else:
                        self.player2.updateQ(reward, self.board, self.possible_moves())

                elif reward == 0:
                    if isPlayer1:
                        self.player1.updateQ(reward, self.board, self.possible_moves())
                    else:
                        self.player2.updateQ(reward, self.board, self.possible_moves())

                isPlayer1 = not isPlayer1  #change player


    #save Qtables
    def saveQtables(self):
        self.player1.saveQtable("./player1Qtable.txt")
        self.player2.saveQtable("./player2Qtable.txt")


class player:
    def __init__(self,epsilon=0.2, alpha=0.3, gamma=0.9):
        self.epsilon=epsilon
        self.alpha=alpha
        self.gamma=gamma
        self.Q = {} #Q table
        self.last_board=None
        self.q_last=0.0
        self.state_action_last=None


    def game_begin(self):
        self.last_board = None
        self.q_last = 0.0
        self.state_action_last = None

    def epslion_greedy(self, state, possible_moves): #esplion greedy algorithm
        #return  action
        self.last_board = tuple(state)
        if(random.random() < self.epsilon):
            move = random.choice(possible_moves) ##action
            self.state_action_last=(self.last_board,move)
            self.q_last=self.getQ(self.last_board,move)
            return move
        else: #greedy strategy
            Q_list=[]
            for action in possible_moves:
                Q_list.append(self.getQ(self.last_board,action))
            maxQ=max(Q_list)

            if Q_list.count(maxQ) > 1:
                # more than 1 best option; choose among them randomly
                best_options = [i for i in range(len(possible_moves)) if Q_list[i] == maxQ]
                i = random.choice(best_options)
            else:
                i = Q_list.index(maxQ)
            self.state_action_last = (self.last_board, possible_moves[i])
            self.q_last = self.getQ(self.last_board, possible_moves[i])
            return possible_moves[i]

    def getQ(self, state, action): #get Q states
        if(self.Q.get((state,action))) is None:
            self.Q[(state,action)] = 1.0
        return self.Q.get((state,action))

    def updateQ(self, reward, state, possible_moves): # update Q states using Qlearning
        q_list=[]
        for moves in possible_moves:
            q_list.append(self.getQ(tuple(state), moves))
        if q_list:
            max_q_next = max(q_list)
        else:
            max_q_next=0.0
        self.Q[self.state_action_last] = self.q_last + self.alpha * ((reward + self.gamma*max_q_next) - self.q_last)

    def saveQtable(self,file_name):  #save table
        Qtable=self.getQtable()
        with open(file_name, 'wb') as handle:
            pickle.dump(Qtable, handle)


    def getQtable(self):
        state_action_value=self.Q
        temp_Qtable={}
        for state_action, value in state_action_value.items():
            curr_state = state_action[0]
            try:
                temp_value=temp_Qtable[curr_state]
                if temp_value<value:
                    temp_Qtable[curr_state]=value
            except:
                temp_Qtable[curr_state]=value
        return temp_Qtable

    def loadQtable(self,file_name): # load table
        with open(file_name, 'rb') as handle:
            self.Q = pickle.load(handle)


if __name__ == '__main__':
    game = TicTacToe() #game instance, True means training
    player1= player() #player1 learning agent
    player2 =player() #player2 learning agent
    game.startTraining(player1,player2) #start training

    game.train(args.iteration) #train
    game.saveQtables()  #save Qtable
