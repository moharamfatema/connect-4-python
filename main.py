from src.model.agent import Agent
from src.view.game import Game

# import pygraphviz as pgv

# main function
agent = Agent()

game_class = Game(agent)
game_class.go()