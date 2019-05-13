import gym
from gym import error, spaces, utils
from gym.utils import seeding
import random
import copy
import sys

class CliffEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    def __init__(self, m = 5, n = 3):
        self.n = n
        self.m = m
        self.map = self._generateMap(self.n, self.m)
	self.sets = self._getSets(self.map, self.n, self.m)
        self.mapAgent = self.map
        self.state = [0, 0]
        self.prev_state = [0, 0]
        self.actions = {0: [1, 0], 1: [-1, 0], 2: [0, 1], 3: [0, -1]}
        self.cliffReward = -100.0
        self.stepReward = -1.0
        self.wallReward = -10.0
        self.winReward = 100.0
    
    def _generateMap(self, n, m):
	map_ = []
        for j in range(n):
	    row = []
	    for i in range(m):
		if j == 0 and i != 0 and i != m-1:
		    row.append('c')    
	        else:
		    row.append('.')
	    map_.append(row)
	return map_

    def _getSets(self, map_, n, m):
	sets = {}
	#Define terminaton point
	sets['end'] = [[0, m-1]]
	sets['cliff'] = []
	sets['passage'] = []
	#Define traps, free passages and obstacles
	for row in range(len(map_)):
	    for col in range(len(map_[row])):
#		print map_[row][col]
		cell = map_[row][col]
		if cell == '.':
		    sets['passage'].append([row, col])
		elif cell == 'c':
  	            sets['cliff'].append([row, col])
	return sets

    def getState(self):
	return self.state[0], self.state[1]

    def reset(self):
        self.state = [0, 0]

    def getAgentMap(self, map_, state):
	carte = []
	for row in range(len(map_)):
            row_ = []
	    for col in range(len(map_[row])):
		if row == state[0] and col == state[1]:
		    row_.append('A')
	        else:
		    row_.append(map_[row][col])
        return carte


    def moveF(self, state, act):
        state[0] += self.actions[act][0]
        state[1] += self.actions[act][1]	
	return state

    def moveB(self, state, act):
	#print 'move back'
        state[0] -= self.actions[act][0]
        state[1] -= self.actions[act][1]	
	return state

    def _tryPos(self, state):
	if state in self.sets['cliff']:
	 #   print 'walls'
	    reward = self.cliffReward
	    confirm = False
	    term = True
	elif state in self.sets['end']:
	    reward = self.winReward
	    confirm = True
	    term = True
	elif state in self.sets['passage']:
            reward = self.stepReward
	    confirm = True
	    term = False
	else:
	    #Else it is walls
	    reward = self.wallReward
	    confirm = False
	    term = False
	return confirm, reward, term

    def step(self, action):
	#save preprev state
        self.preprev_state = copy.deepcopy(self.prev_state)
	self.prev_state = copy.deepcopy(self.state)
	#Perform a move
	self.state = self.moveF(self.state, action)
	#Investigate new position, get reward, check if there are no walls and obstacles, if this is a termination
	confirm, reward, term = self._tryPos(self.state)
	#If obstacles or walls then moveB
	if confirm == False:
	    self.state = self.moveB(self.state, action)
        #Draw new state on agent's map
        self.mapAgent = self.map
	self.mapAgent = self.getAgentMap(self.mapAgent, self.state)
	#Otherwise, this is an usual step
	#print self.state
        return self.state, reward, term, ''

    def render(self, mode = 'human', psg = []):
	for i, line in enumerate(self.map):
	    lineStr = ''
	    print ' '
            for j, el in enumerate(line):		
		if [i, j] in psg:
		    lineStr += 'A  '
		else:
		    lineStr += el + '  '
	    print lineStr

    def close(self):
	pass
