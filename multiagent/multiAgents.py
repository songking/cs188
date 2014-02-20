# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
	"""
		A reflex agent chooses an action at each choice point by examining
		its alternatives via a state evaluation function.

		The code below is provided as a guide.  You are welcome to change
		it in any way you see fit, so long as you don't touch our method
		headers.
	"""


	def getAction(self, gameState):
		"""
		You do not need to change this method, but you're welcome to.

		getAction chooses among the best options according to the evaluation function.

		Just like in the previous project, getAction takes a GameState and returns
		some Directions.X for some X in the set {North, South, West, East, Stop}
		"""
		# Collect legal moves and successor states
		legalMoves = gameState.getLegalActions()

		# Choose one of the best actions
		scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
		bestScore = max(scores)
		bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
		chosenIndex = random.choice(bestIndices) # Pick randomly among the best

		"Add more of your code here if you want to"

		return legalMoves[chosenIndex]

	def evaluationFunction(self, currentGameState, action):
		"""
		Design a better evaluation function here.

		The evaluation function takes in the current and proposed successor
		GameStates (pacman.py) and returns a number, where higher numbers are better.

		The code below extracts some useful information from the state, like the
		remaining food (newFood) and Pacman position after moving (newPos).
		newScaredTimes holds the number of moves that each ghost will remain
		scared because of Pacman having eaten a power pellet.

		Print out these variables to see what you're getting, then combine them
		to create a masterful evaluation function.
		"""
		# Useful information you can extract from a GameState (pacman.py)
		successorGameState = currentGameState.generatePacmanSuccessor(action)
		newPos = successorGameState.getPacmanPosition()
		newFood = successorGameState.getFood()
		newGhostStates = successorGameState.getGhostStates()
		newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
	

		"*** YOUR CODE HERE ***"
		if successorGameState.isWin():
			return 99999

		x,y = newPos
		score = successorGameState.getScore()
		currGhostPosition = currentGameState.getGhostPosition(1)
		ghostDistance = util.manhattanDistance(currGhostPosition, newPos)
		walls = currentGameState.getWalls()
		for scaredTimes in newScaredTimes:
			if ghostDistance <= scaredTimes:
				score += ghostDistance**2        
		#if ghostDistance <= 3:
			#score += ghostDistance
		foodList = newFood.asList()
		remainingFood = successorGameState.getNumFood()
		if remainingFood < currentGameState.getNumFood():
			score += 10
		closestFood = float("inf")
		if remainingFood > 0:
			for food in foodList:
				closestFood = min(closestFood, util.manhattanDistance(food,newPos))
			score += 1.0/closestFood
		powerPellets = currentGameState.getCapsules()
		if newPos in powerPellets:
			score += 100
		for scaredTimes in newScaredTimes:
				score += scaredTimes
		if action == Directions.STOP:
				score -= 1000
		x,y = newPos
		if walls[x][y]:
			score -= 1000    		
		return score



def scoreEvaluationFunction(currentGameState):
	"""
		This default evaluation function just returns the score of the state.
		The score is the same one displayed in the Pacman GUI.

		This evaluation function is meant for use with adversarial search agents
		(not reflex agents).
	"""
	return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
	"""
		This class provides some common elements to all of your
		multi-agent searchers.  Any methods defined here will be available
		to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

		You *do not* need to make any changes here, but you can if you want to
		add functionality to all your adversarial search agents.  Please do not
		remove anything, however.

		Note: this is an abstract class: one that should not be instantiated.  It's
		only partially specified, and designed to be extended.  Agent (game.py)
		is another abstract class.
	"""

	def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
			self.index = 0 # Pacman is always agent index 0
			self.evaluationFunction = util.lookup(evalFn, globals())
			self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
	"""
		Your minimax agent (question 2)
	"""

	def getAction(self, gameState):
		"""
			Returns the minimax action from the current gameState using self.depth
			and self.evaluationFunction.

			Here are some method calls that might be useful when implementing minimax.

			gameState.getLegalActions(agentIndex):
				Returns a list of legal actions for an agent
				agentIndex=0 means Pacman, ghosts are >= 1

			gameState.generateSuccessor(agentIndex, action):
				Returns the successor game state after an agent takes an action

			gameState.getNumAgents():
				Returns the total number of agents in the game
		"""
		"*** YOUR CODE HERE ***"
		actions = gameState.getLegalActions(0)
		v = float('-inf')
		nextAction = Directions.STOP
		for action in actions:
			temp = self.minValue(0, 1, gameState.generateSuccessor(0, action))
			if temp > v:
				v = temp
				nextAction = action
		return nextAction


	def maxValue(self, depth, agent, gameState):
		if depth == self.depth or gameState.isWin() or gameState.isLose():
			return self.evaluationFunction(gameState)
		actions = gameState.getLegalActions(agent)
		if len(actions) == 0:
			return self.evaluationFunction(gameState)
		v = float('-inf')
		for action in actions:
			v = max(v, self.minValue(depth, agent+1, gameState.generateSuccessor(agent, action)))
		return v


	def minValue(self, depth, agent, gameState):
		if depth == self.depth or gameState.isWin() or gameState.isLose():
			return self.evaluationFunction(gameState)
		actions = gameState.getLegalActions(agent)
		if len(actions) == 0:
			return self.evaluationFunction(gameState)
		v = float('inf')
		for action in actions:
			if agent == gameState.getNumAgents() - 1:
				temp = self.maxValue(depth + 1, 0, gameState.generateSuccessor(agent, action))
			else:
				temp = self.minValue(depth, agent + 1, gameState.generateSuccessor(agent, action))
			v = min(v,temp)
		return v

class AlphaBetaAgent(MultiAgentSearchAgent):
	"""
		Your minimax agent with alpha-beta pruning (question 3)
	"""

	def getAction(self, gameState):
		"""
			Returns the minimax action using self.depth and self.evaluationFunction
		"""
		"*** YOUR CODE HERE ***"
		actions = gameState.getLegalActions(0)
		v = float('-inf')
		alpha = float('-inf')
		beta = float('inf')
		nextAction = Directions.STOP
		for action in actions:
			temp = self.minValue(0, 1, gameState.generateSuccessor(0, action), alpha, beta)
			if temp > v:
				v = temp
				nextAction = action
			if v > beta:
				return nextAction
			alpha = max(alpha,v)
		return nextAction


	def maxValue(self, depth, agent, gameState, alpha, beta):
		if depth == self.depth or gameState.isWin() or gameState.isLose():
			return self.evaluationFunction(gameState)
		actions = gameState.getLegalActions(agent)
		if len(actions) == 0:
			return self.evaluationFunction(gameState)
		v = float('-inf')
		for action in actions:
			v = max(v, self.minValue(depth, agent+1, gameState.generateSuccessor(agent, action), alpha, beta))
			if v > beta:
				return v
			alpha = max(alpha, v)
		return v


	def minValue(self, depth, agent, gameState, alpha, beta):
		if depth == self.depth or gameState.isWin() or gameState.isLose():
			return self.evaluationFunction(gameState)
		actions = gameState.getLegalActions(agent)
		if len(actions) == 0:
			return self.evaluationFunction(gameState)
		v = float('inf')
		for action in actions:
			if agent == gameState.getNumAgents() - 1:
				temp = self.maxValue(depth + 1, 0, gameState.generateSuccessor(agent, action), alpha, beta)
			else:
				temp = self.minValue(depth, agent + 1, gameState.generateSuccessor(agent, action), alpha, beta)
			v = min(v,temp)
			if v < alpha:
				return v
			beta = min(beta,v)
		return v

class ExpectimaxAgent(MultiAgentSearchAgent):
	"""
		Your expectimax agent (question 4)
	"""

	def getAction(self, gameState):
		"""
			Returns the expectimax action using self.depth and self.evaluationFunction

			All ghosts should be modeled as choosing uniformly at random from their
			legal moves.
		"""
		"*** YOUR CODE HERE ***"
		actions = gameState.getLegalActions(0)
		v = float('-inf')
		nextAction = Directions.STOP
		for action in actions:
			temp = self.expValue(0, 1, gameState.generateSuccessor(0, action))
			if temp > v:
				v = temp
				nextAction = action
		return nextAction


	def maxValue(self, depth, agent, gameState):
		if depth == self.depth or gameState.isWin() or gameState.isLose():
			return self.evaluationFunction(gameState)
		actions = gameState.getLegalActions(agent)
		if len(actions) == 0:
			return self.evaluationFunction(gameState)
		v = float('-inf')
		for action in actions:
			v = max(v, self.minValue(depth, agent+1, gameState.generateSuccessor(agent, action)))
		return v


	def minValue(self, depth, agent, gameState):
		if depth == self.depth or gameState.isWin() or gameState.isLose():
			return self.evaluationFunction(gameState)
		actions = gameState.getLegalActions(agent)
		if len(actions) == 0:
			return self.evaluationFunction(gameState)
		v = float('inf')
		for action in actions:
			if agent == gameState.getNumAgents() - 1:
				temp = self.maxValue(depth + 1, 0, gameState.generateSuccessor(agent, action))
			else:
				temp = self.minValue(depth, agent + 1, gameState.generateSuccessor(agent, action))
			v = min(v,temp)
		return v

	def expValue(self, depth, agent, gameState):
		if depth == self.depth or gameState.isWin() or gameState.isLose():
			return self.evaluationFunction(gameState)
		actions = gameState.getLegalActions(agent)
		numActions = len(actions)
		if numActions == 0:
			return self.evaluationFunction(gameState)
		v = 0
		for action in actions:
			if agent == gameState.getNumAgents() - 1:
				v += self.maxValue(depth + 1, 0, gameState.generateSuccessor(agent, action))
			else:
				v += self.expValue(depth, agent + 1, gameState.generateSuccessor(agent, action))
		v = float(v)/float(len(actions))
		return v

def betterEvaluationFunction(currentGameState):
		"""
			Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
			evaluation function (question 5).

			- Our "better" evaluation function is actually just a modified version of our reflex agent.
			- The evaluation function returns a linear combination of different features.
			- These features are:
			- Distance to nearest ghost (if distance is less than or equal to 3 or that ghost's scared time)
			- Reciprocal of distance to nearest food
			- If current position (currPos) is a power pellet
			- Current scared times of all ghosts
			

		"""
		"*** YOUR CODE HERE ***"
		# Useful information you can extract from a GameState (pacman.py)
		currPos = currentGameState.getPacmanPosition()
		food = currentGameState.getFood()
		ghostStates = currentGameState.getGhostStates()
		currScaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
	
		if currentGameState.isWin():
			return 99999

		x,y = currPos
		score = currentGameState.getScore()
		currGhostPosition = currentGameState.getGhostPosition(1)
		ghostDistance = util.manhattanDistance(currGhostPosition, currPos)
		walls = currentGameState.getWalls()
		for scaredTimes in currScaredTimes:
			if ghostDistance <= scaredTimes:
				score += ghostDistance**2
				score += scaredTimes        
		if ghostDistance <= 3:
			score += ghostDistance
		foodList = food.asList()
		remainingFood = currentGameState.getNumFood()
		closestFood = float("inf")
		if remainingFood > 0:
			for food in foodList:
				closestFood = min(closestFood, util.manhattanDistance(food,currPos))
			score += 1.0/closestFood
		powerPellets = currentGameState.getCapsules()
		if currPos in powerPellets:
			score += 100	
		return score

# Abbreviation
better = betterEvaluationFunction

