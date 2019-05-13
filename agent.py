import random
import copy
from datetime import datetime

class Agent:
    def __init__(self, m = 11, n = 4):
	#Discount factor // 0 - considering current rewards // 1 - stive for  long-term high reward
        self.gamma = 0.5
	#Learning rate // 0 nothing to learn // considering only new info
        self.alpha = 0.5
        self.n = n
        self.m = m
        self.nStates = 4
        self.actions = {0: [1, 0], 1: [-1, 0], 2: [0, 1], 3: [0, -1]}
        #There four actions up, down, left, right
        self.Q = self._initQ(self.n, self.m, self.nStates)
        self.cnt = 0.9

    def _initQ(self, n, m, nStates):
        '''Randomly initializate Q values'''
        random.seed()
	Q = []
        for i in range(n):
            row = []
            for j in range(m):
                Qsa = []
                for k in range(nStates):
                    Qsa.append(round(random.random(), 2))
                row.append(Qsa)
            Q.append(row)
        return Q

    def reset(self):
        self.Q = self._initQ(self.n, self.m, self.nStates)

    def getQtable(self):
	return self.Q

    def getExploitationSteps(self, n):
        psg = [[0,0]]
	st = [0, 0]
	for step in range(n):
	    act = self.act(st, 0)
	    st[0] = st[0] + self.actions[act][0]
	    st[1] = st[1] + self.actions[act][1]
	    psg.append(copy.deepcopy(st))
	    if st[0] > self.n-1 or st[1] >self.m-1 or st[0] < 0 or st[1] < 0:
                break
	return psg

    def act(self, state, eps):
	#Epsilon-greedy action choosing
        if random.random() > eps:

            max_val = max(self.Q[state[0]][state[1]])

	    cnt = [q for q in self.Q[state[0]][state[1]] if q == max_val]
	    if len(cnt) == 1:
                action = self.Q[state[0]][state[1]].index(max_val)	
	    else:
		action = random.randint(0, 3)
	else: 
	    action = random.randint(0, 3)

	self.cnt += 1

        return action

    def update(self, s_, s, a_, a, r, alg = 'SARSA'):
	if alg == 'SARSA':
	    x = self.Q[s_[0]][s_[1]][a_]
	elif alg == 'QL':
	    max_val = max(self.Q[s_[0]][s_[1]])
	    #if there are several same values in Q-table
	    cnt = [q for q in self.Q[s_[0]][s_[1]] if q == max_val]
	    if len(cnt) == 1:
                x = self.Q[s_[0]][s_[1]].index(max_val)	#
	    else:
		ind = []
		for j in range(len(self.Q[s_[0]][s_[1]])):
		    if self.Q[s_[0]][s_[1]][j] == max_val:
			ind.append(j)
		x = ind[random.randint(0, len(ind)-1)]
        error = r + self.gamma * x - self.Q[s[0]][s[1]][a]
	self.Q[s[0]][s[1]][a] += self.alpha*(error)
	self.Q[s[0]][s[1]][a] = round(self.Q[s[0]][s[1]][a], 2)
