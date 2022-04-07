from model.agent import Agent
from view.main_frame import MainFrame
from view.game import Game

# main function
agent = Agent()
frame = MainFrame(agent)
game_class = Game(agent, frame)
game_class.go()