import gym
import gym_cliff
from agent import Agent
import matplotlib.pyplot as plt
import random
import copy 
from datetime import datetime

class Learning:
    def __init__(self):
        random.seed()
        self.m = 5
        self.n = 3
        self.env = gym.make('cliff-v0')
	self.agent = Agent(self.m, self.n)
        self.epReturn = []
        self.nEpisodes = 1000

    def run(self):
        i = 0
        for episode in range(self.nEpisodes):
	    self.env.reset()
            eps = max(0.01, 0.95 - float(episode)/500)
            #Get initial state
            s_prev = self.env.getState()
            a_prev = self.agent.act(s_prev, eps)
	    #print 'Episode number', episode
            curReturn = 0
	    term = False
   	    t = datetime.now().microsecond
  	    i += 1
            while term == False:
	        '''In notions of Sutton's book a_new = A', a_prev = A, same for states
                Gets reward and moves to another state'''
	        #Was in, performed an action
   	        #print  s_prev, a_prev
                s_new, r, term, info = self.env.step(a_prev)
#	        if s_new == [0, self.m-1]:
#	            print 'ONCE', term, r, s_new

    	        #Choose a_new from s_new
                a_new = self.agent.act(s_new, eps)

                #Q values are updated

                self.agent.update(s_new, s_prev, a_new, a_prev, r)

	        #print 'Step number', step, s_new, s_prev, a_prev, r
                #New state to take the action in the beginning
	        s_prev = copy.deepcopy(s_new)
	        a_prev = copy.deepcopy(a_new)
                #Env visualizes movements
  	        #env.render()
	        curReturn += r

            self.epReturn.append(curReturn)
	t -= datetime.now().microsecond
        self._visualize()

    def _visualize(self):
        for line in self.agent.getQtable():
            print line
        passages = self.agent.getExploitationSteps(20)
        print passages
        plt.plot(self.epReturn, 'r*')
        plt.show()

if __name__ == '__main__':
    process = Learning()
    process.run()
