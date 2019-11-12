# COMP_560_HW2
Group members: Zheng Qi, Hongyu Su, Julia Tian

After reading the reinforcement methods that could be used to train the agent in the 3D Tic-Tac-Toe like minimax, TD learning and Q-learning. We decided to use Q-learning since we do not know every policy we need to use at each state. We used the epsilon greedy method to balance the exploration and exploitation. At the initial stage, the agent might try more states to explore. But during late time, it would choose the action that maximizes Q-value for all possible moves at that state, which is exploitation. I would go deep to this when explaining code.

For code, we first initiated a TicTacToe class and created a board which was the list that contain 64 empty space(4*4*4), indexing from 0 to 63. We had fields “done” to test whether any player win or and “player1” and “player2” for later training. We defined a few functions needed. We first implemented “evaluate function” which takes tic-tac-toe self and current playername (‘x’/’o’) as parameters. We first checked the 4 2D planes, checking every row/column/diagonal. Then we checked the 3d space. We first checked the vertical lines and horizontal lines in 3D. And then the peripheral of the base 4*4 square to see whether “x”/”o” could make a line up in 3D. If a player made a line, we would return reward=1 and done=true. If it ties, ie all places filled but nobody wins, we reward=0.5, else reward=0.Next, we defined a function “possible moves” which enumerated the board to check any space was empty and returned the index of empty spaces to be next possible moves. We then defined function ‘step’  which takes in tictactoe self, the name of player, and next move index in range 0-63 as parameters. If the next move try to overwrite existing value(‘o’/’x’) we would punish it with reward=-5. Then we marked that index of board with the player’s name and evaluated this position and return the corresponding reward and done. Ie, the use of the step function is to according to move index, take that space and evaluated that action and returned its corresponding reward and its done or not.

Before we started training, we need to use Q-learning to decide the next move and also updated Q table to find final utility. We defined a class called player which basic did Q learning stuff. We initiated it with epsilon=0.2, alpha=0.3 and gamma =0.9. We created a Q table which was a dictionary that took the (state, action) as key and corresponding Q-value as values. We also has last_board field to store the last state and q_last field to store the last q value and state_action_last to store the latest (state,action). With “game_begin” method we initialized all those fields to be none. We then implemented the getQ function which require( state,action) as key to get the associated q-value. If q-value doesn’t exist, we initialize that to 1. Next, we implemented the epsilon greedy method to find the next action to be done given current state. Hence, we took the self, current state, possible moves related to that states as parameters. For exploration, if random number smaller than epsilon, we would randomly choose an index in possible_moves lists as next action and we updated the state_action_last field to be the tuple(current state, next_move place) and q_last to be call the get Q function with (current state, next_move place) to get the associated current q value. Else we would go exploitation that we find q values for every possible (move index and current state) tuple. We choose the action(ie possbile_values[i]) given current states that return the max Q-value to be next action. We then updated latest_action_last field and latest q field correspondingly. For this function, We return the next action to do based on current states and possible moves.
Now we implemented the updateQ function which took in the reward, state and possible_moves as parameter. We first calculated the largest q-value given the state and possible moves and updated the Q table through bellman equation which was  Q(s,a) ← Q(s,a) + α(R(s) + γ Q(s′,a′) − Q(s,a)) iteratively.

Now we have all functions need and we can write train function. While not done, we decide the player and called the epsilon_greedy function to decide the next action. The epsilon_greedy function store the field “latest q” and “latest ( state,action)” that corresponding to current state and the action decide to take. Those fields would be used in later Q updated. We then called” step function” which takes in the player and the new action did. Now next self.board and self.possible _moves would all updated because a new space was taken. This function return rewards based on the evaluation of this move. If reward==1,
                   # won
                    if isPlayer1:
                        self.player1.updateQ(reward, self.board, self.possible_moves())
                        self.player2.updateQ(-1 * reward, self.board, self.possible_moves())
                    else:
                        self.player1.updateQ(-1 * reward, self.board, self.possible_moves())
                        self.player2.updateQ(reward, self.board, self.possible_moves())

So we updated player1, player 2 q table simultaneous with winner get reward=1. And loser get reward=-1. 
#def updateQ(self, reward, state, possible_moves): # update Q states using Q-learning
        q_list=[]
        for moves in possible_moves:
            q_list.append(self.getQ(tuple(state), moves))
        if q_list:
            max_q_next = max(q_list)
        else:
            max_q_next=0.0
        self.Q[self.state_action_last] = self.q_last + self.alpha * ((reward + self.gamma*max_q_next) - self.q_last)

Since the self.board and self.possible_moves are updated after the step function, we could updated Q tables ie. calculate Q(last state_action) based on q_last stored in the greedy function and max_q_next we get from current updated state and possible moves.	
Then for other reward cases ie not done, tie, illegal move, we just call updatedQ	to updated Q table correspondingly.

With enough iterations. We can get good Q-tables for player1 and player2 and we can choose the U (s) = max Q(s, a)  as our utility function. For special cases mentioned in the pdf, ie 3 in a row or 2 in a row. If that happens a few times and lead to loss, the utility value at that (state,action) would be really low for its opposites and from Q-learning, the agent will automatically tried best to avoid that because it prefers Max Q value. I mean player would try to avoid that situation after a few times trials. 
				

Hongyu Su: co-programming with Zheng-Qi for the Q-learning and greedy epsilon method and write reports
Zheng Qi:
Julia Tian:	
		
