# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        

        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        
        self.values = util.Counter() 
        for i in range(self.iterations): #i stands for iteration
          allstates = self.mdp.getStates()
          VK_subtract_1 = self.values.copy()
          for s in allstates: #s stands for state
            values_of_actions = util.Counter()
            isterminalstate = self.mdp.isTerminal(s)
            if isterminalstate == False:
              all_actions = self.mdp.getPossibleActions(s)
              for a in all_actions: #action is represented by an a
                TransitionStatesAndProbs = self.mdp.getTransitionStatesAndProbs(s, a)
                for transition in TransitionStatesAndProbs:
                  NextState, stateprobability = transition
                  discount = self.discount
                  reward = self.mdp.getReward(s, a, NextState)
                  values_of_actions[a] = values_of_actions[a] + stateprobability * (reward + (discount * VK_subtract_1[NextState]))
              maxActionValues = values_of_actions.argMax()
              self.values[s] = values_of_actions[maxActionValues]


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        
        isterminalstate = self.mdp.isTerminal(state)
        value_of_Q = 0.0
        

        if isterminalstate is False:
          for transition in self.mdp.getTransitionStatesAndProbs(state,action):
            next_state, prob = transition
            reward = self.mdp.getReward(state,action,next_state)
            discount = self.discount
            value_of_Q = value_of_Q + prob * (reward + (discount * self.values[next_state])) 
        return value_of_Q

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        QValueMax = -10000000000000.0
        optimal_action = None
            
        for a in self.mdp.getPossibleActions(state): # a is actions; self.mdp.getPossibleActions(state) gives you all of the actions
            temporary = self.getQValue(state, a)
            if QValueMax <= temporary:
                QValueMax = temporary
                optimal_action = a
        return optimal_action


    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
