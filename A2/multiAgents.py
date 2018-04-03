
# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
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
        if action == 'Stop':
            return float("-inf")
        newGhostPostions = successorGameState.getGhostPositions()
        score = successorGameState.getScore()

        foods = newFood.asList()
        if len(foods) > 0:
            foodDistance = [manhattanDistance(newPos, food) for food in newFood.asList()]
            score += 2/float(min(foodDistance)) + 10/float(sum(foodDistance))

        for i in range(0,len(newGhostStates)):
            distance = manhattanDistance(newGhostPostions[i], newPos)
            score += min(3, distance)*100
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
        def minimax(state, depth, cur_agent):
            if cur_agent == 0:
                value = float('-inf')
                depth += 1
            else:
                value = float('inf')
            best_action = None

            if depth == self.depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state), best_action

            for action in state.getLegalActions(cur_agent):
                next_state = state.generateSuccessor(cur_agent, action)
                next_val, next_action = minimax(next_state, depth, (cur_agent+1) % state.getNumAgents())
                if cur_agent == 0 and next_val > value:
                    value, best_action = next_val, action
                if cur_agent != 0 and next_val < value :
                    value, best_action = next_val, action
            return value, best_action

        value, best_action = minimax(gameState, -1, 0)

        return best_action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def alphabeta(state, depth, cur_agent, alpha, beta):
            if cur_agent == 0:
                value = float('-inf')
                depth += 1
            else:
                value = float('inf')
            best_action = None

            if depth == self.depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state), best_action

            for action in state.getLegalActions(cur_agent):
                next_state = state.generateSuccessor(cur_agent, action)
                next_val, next_action = alphabeta(next_state, depth, (cur_agent+1) % state.getNumAgents(), alpha, beta)
                if cur_agent == 0:
                    if next_val > value:
                        value, best_action = next_val, action
                    if value >= beta:
                        return value, best_action
                    alpha = max(alpha, value)
                if cur_agent != 0:
                    if next_val < value :
                        value, best_action = next_val, action
                    if value <= alpha:
                        return value, best_action
                    beta = min(beta, value)
            return value, best_action

        value, best_action = alphabeta(gameState, -1, 0, float('-inf'), float('inf'))

        return best_action

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
        def expectimax(state, depth, cur_agent):
            if cur_agent == 0:
                value = float('-inf')
                depth += 1
            else:
                value = 0
            best_action = None

            if depth == self.depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state), best_action

            action_num = 0
            for action in state.getLegalActions(cur_agent):
                next_state = state.generateSuccessor(cur_agent, action)
                next_val, next_action = expectimax(next_state, depth, (cur_agent+1) % state.getNumAgents())
                if cur_agent == 0 and (next_val > value or (next_val == value and best_action == "Stop")):
                    value, best_action = next_val, action
                if cur_agent != 0:
                    value += next_val
                    action_num += 1
            if cur_agent != 0 and action_num > 1:
                value /= float(action_num)
            return value, best_action

        expectimax_value, expectimax_action = expectimax(gameState, -1, 0)
        return expectimax_action

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: The evaluation function based on the distance between pacman
      and the cloest food and the sum of dictances between pacman and all foods
      left. If the pacman pass by a capsule, it will highly evaluate eating the
      capsule and then chasing the scared ghost. The pacman will consider a
      ghost to be dangerous if it is less than 4 steps away from itself and
      it will try to avoid the ghost only when that happened.
    """
    "*** YOUR CODE HERE ***"

    curPos = currentGameState.getPacmanPosition()
    curFood = currentGameState.getFood()
    curGhostStates = currentGameState.getGhostStates()
    curScaredTimes = [ghostState.scaredTimer for ghostState in curGhostStates]
    curGhostPostions = currentGameState.getGhostPositions()

    score = currentGameState.getScore()

    if currentGameState.isLose():
        score -= 10000

    foods = curFood.asList()
    if len(foods) > 0:
        foodDistance = [manhattanDistance(curPos, food) for food in curFood.asList()]
        score += 10/float(min(foodDistance)) + 20/float(sum(foodDistance))

    capsules = currentGameState.getCapsules()
    if len(capsules) != 0:
        score += 300/float(len(capsules))
        cloest_capsule = min([manhattanDistance(curPos, capsule) for capsule in capsules])
        if cloest_capsule < 4:
            score += 20/float(cloest_capsule)
    if len(capsules) == 0:
        score += 400
    for i in range(0,len(curGhostStates)):
        distance = manhattanDistance(curGhostPostions[i], curPos)
        if curScaredTimes[i] > distance:
            score += 100/distance
        else:
            if distance > 2:
                score += distance * 0.02
            else:
                score += distance * 20
    return score


# Abbreviation
better = betterEvaluationFunction
