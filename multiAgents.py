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
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

    def evaluationFunction(self, currentGameState: GameState, action):
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
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState: GameState):
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
    
    def getAction(self, gameState: GameState):
        PACMAN = 0  # Pacman在代理中的索引初始值

        def max_PACMAN(state, depth):
            if state.isWin() or state.isLose():  # 如果狀態已經是勝利或失敗狀態，則直接返回狀態的得分
                return state.getScore()
            actions = state.getLegalActions(PACMAN)  # 獲取合法的行動
            score = best_score = float("-inf")  # 初始分數為負無窮
            best_action = Directions.STOP  # 初始行動為停止
            for action in actions:  # 遍歷所有合法行動，找到最好的行動並計算分數，找出max分數值
                score = min_ghost(state.generateSuccessor(PACMAN, action), depth, 1) # 分數是找ghost中最大的分數
                if score > best_score: # PACMAN是找max，找最大的分數及行動
                    best_score = score
                    best_action = action
            if depth == 0:
                return best_action  # 最後一層搜索，返回行動
            else:
                return best_score # 不是最後一層搜索，返回分數
            
        def min_ghost(state, depth, ghost):
            if state.isLose() or state.isWin():  # 如果狀態已經是勝利或失敗狀態，則直接返回狀態的得分
                return state.getScore()
            next_ghost = ghost + 1  # 下一個鬼的索引
            if ghost == state.getNumAgents() - 1:  # 如果當前智能體是最後一個智能體，則下一個智能體是Pacman智能體
                next_ghost = PACMAN
            actions = state.getLegalActions(ghost)  # 獲取合法的行動
            score = best_score = float("inf")  # 初始值為正無窮
            for action in actions:  # 遍歷所有合法行動，找到最好的行動
                if next_ghost == PACMAN:  # 如果下一個是Pacman，繼續向下搜尋
                    if depth == self.depth - 1:  # 如果已經到達搜索深度的上限直接計算分數
                        score = self.evaluationFunction(state.generateSuccessor(ghost, action))
                    else:
                        score = max_PACMAN(state.generateSuccessor(ghost, action), depth + 1)  # 否則繼續向下搜索
                else:  # 如果下一個是鬼，則繼續搜索期望值
                    score = min_ghost(state.generateSuccessor(ghost, action), depth, next_ghost)
                if score < best_score: # 鬼是找min，找最小的分數
                    best_score = score
            return best_score  # 返回最好的分數

        return max_PACMAN(gameState, 0)  # 返回最好的行動


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
