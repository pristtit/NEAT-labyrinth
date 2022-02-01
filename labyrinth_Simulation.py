import os
import neat
import labyrinth
import visualize
from PIL import Image, ImageDraw, ImageFont
import keyboard
try:
    import cPickle as pickle
except ImportError:
    import pickle

def run(config_file):

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    with open(input('Введите имя открываемого файла(тип Pickle): ')+'.pickle', 'rb') as f:
        winner = pickle.load(f)
    labyrinth.simul(winner, config)
    node_names = {-1:'1', -2: '2', -3:'3', -4:'4', -5:'5', -6:'6', -7:'7', -8:'8', 0:'N0', 1:'N1', 2:'N2', 3:'N3'}
    visualize.draw_net(config, winner, True, node_names=node_names)
    print('\nBest genome:\n{!s}'.format(winner))

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)