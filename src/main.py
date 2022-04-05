from model.agent import Agent
from view.game import Game

# main function
agent = Agent()

game_class = Game(agent)
game_class.go()