import os
import neat
import visualize
from PIL import Image, ImageDraw, ImageFont
import keyboard
try:
    import cPickle as pickle
except ImportError:
    import pickle

class sreda:

    def __init__(self, ):
        self.stena = dict.fromkeys(['00','10','20','30','40','50','60','70','80','90','91','92','93','94','95','96','97','98','99','89','79','69',
                                '59','49','39','29','19','09','08','07','06','05','04','03','02','01'], False)

        self.plosh = dict.fromkeys(['58','57','56','46','36','26','25','24','23','43','44','45','31','41','51','61','62','63','74','75',
                                    '76','77'], False)
        self.plosh.update(self.stena)
        self.test = dict.fromkeys(['16', '12', '32', '54', '68', '88', '83'], True)
        self.start = ((4,8,0),(1,4,2),(2,2,0),(3,5,2),(5,3,2),(6,5,3),(7,8,1),(7,3,3))
        self.shag = 60
        self.kolvo = 560
sreda = sreda()

def eval_genomes(genomes, config):

    for genome_id, genome in genomes:
        karti = sreda.start
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        test = sreda.test
        plosh = sreda.plosh
        for karta in karti:
            ploshygebil = {}
            coord1 = karta[0]
            coord2= karta[1]
            k =  karta[2]
            for shag in range(sreda.shag):
                up = [coord1, coord2 + 1]
                down = [coord1, coord2 - 1]
                left = [coord1 + 1, coord2]
                right = [coord1 - 1, coord2]
                alfa = k % 4
                ploshygebil[str(coord1)+str(coord2)] = True
                if alfa == 0:
                    pass
                #down
                elif alfa == 2:
                    up, down, left, right = down, up, right, left
                #left
                elif alfa == 3:
                    up, down, left, right = left, right, down, up
                #right
                elif alfa == 1:
                    up, down, left, right = right, left, up, down
                radius = [str(up[0])+str(up[1]), str(down[0])+str(down[1]), str(left[0])+str(left[1]), str(right[0])+str(right[1])]
                vhod = [0,0,0,0,0,0,0,0]
                for nomer, i in enumerate(radius):
                    if plosh.get(i, 1) == False:
                        vhod[nomer] = 1
                    else:
                        vhod[nomer] = 0
                    if ploshygebil.get(i) == True:
                        vhod[nomer+4] = 1
                    else:
                        vhod[nomer+4] = 0
                output = net.activate(vhod)
                if output.index(max(output)) == 0:
                    pass
                elif output.index(max(output)) == 1:
                    k += 1
                elif output.index(max(output)) == 2:
                    k += 2
                elif output.index(max(output)) == 3:
                    k += 3
                alfa = k % 4
                up = [coord1, coord2 + 1]
                down = [coord1, coord2 - 1]
                left = [coord1 + 1, coord2]
                right = [coord1 - 1, coord2]
                #down
                if alfa == 2:
                    up, down, left, right = down, up, right, left
                #left
                elif alfa == 3:
                    up, down, left, right = left, right, down, up
                #right
                elif alfa == 1:
                    up, down, left, right = right, left, up, down
                if not plosh.get(str(up[0])+str(up[1]),1):
                    break
                coord1, coord2 = up
                if test.get(str(coord1)+str(coord2),False) and not ploshygebil.get(str(coord1)+str(coord2),False):
                    genome.fitness += 10


def simul(genomes, config):

    genome = genomes
    karti = sreda.start
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    test = sreda.test
    plosh = sreda.plosh
    for karta in karti:
        new_img = Image.new('RGB', (1001, 1001), 'black')
        pencil = ImageDraw.Draw(new_img)
        font = ImageFont.load_default()
        for x in range(0,1000,100):
            for y in range(0,1000,100):
                if str(int(x/100))+str(int(y/100)) in test.keys():
                    pencil.rectangle((x, y, x+100, y+100), fill='white')
                if str(int(x/100))+str(int(y/100)) in plosh.keys():
                    pencil.rectangle((x, y, x+100, y+100), fill='green')
                pencil.rectangle((x, y, x+100, y+100), outline ='green')
                pencil.text((x,y), str(int(x/100))+str(int(y/100)), font=font, fill='blue', size = 288)
        ploshygebil = {}
        coord1 = karta[0]
        coord2= karta[1]
        k = karta[2]
        for shag in range(sreda.shag):
            if ploshygebil.get(str(coord1)+str(coord2),False):
                pencil.text((coord1*100+50, coord2*100+40),str(shag),  font=font, fill='blue', size = 288)
            else:
                pencil.ellipse((coord1*100+10, coord2*100+10, coord1*100+100-10, coord2*100+100-10), fill ='red')
                pencil.text((coord1*100+50, coord2*100+50),str(shag),  font=font, fill='blue', size = 288)
            up = [coord1, coord2 + 1]
            down = [coord1, coord2 - 1]
            left = [coord1 + 1, coord2]
            right = [coord1 - 1, coord2]
            alfa = k % 4
            ploshygebil[str(coord1)+str(coord2)] = True
            if alfa == 0:
                pass
            #down
            elif alfa == 2:
                up, down, left, right = down, up, right, left
            #left
            elif alfa == 3:
                up, down, left, right = left, right, down, up
            #right
            elif alfa == 1:
                up, down, left, right = right, left, up, down
            radius = [str(up[0])+str(up[1]), str(down[0])+str(down[1]), str(left[0])+str(left[1]), str(right[0])+str(right[1])]
            vhod = [0,0,0,0,0,0,0,0]
            for nomer, i in enumerate(radius):
                if plosh.get(i, 1) == False:
                    vhod[nomer] = 1
                else:
                    vhod[nomer] = 0
                if ploshygebil.get(i) == True:
                    vhod[nomer+4] = 1
                else:
                    vhod[nomer+4] = 0
            output = net.activate(vhod)
            if output.index(max(output)) == 0:
                pass
            elif output.index(max(output)) == 1:
                k += 1
            elif output.index(max(output)) == 2:
                k += 2
            elif output.index(max(output)) == 3:
                k += 3
            alfa = k % 4
            up = [coord1, coord2 + 1]
            down = [coord1, coord2 - 1]
            left = [coord1 + 1, coord2]
            right = [coord1 - 1, coord2]
            #down
            if alfa == 2:
                up, down, left, right = down, up, right, left
            #left
            elif alfa == 3:
                up, down, left, right = left, right, down, up
            #right
            elif alfa == 1:
                up, down, left, right = right, left, up, down
            if not plosh.get(str(up[0])+str(up[1]),1):
                break
            coord1, coord2 = up
        new_img.show()


def run(config_file):

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    p.add_reporter(neat.Checkpointer())
    node_names = {-1:'1', -2: '2', -3:'3', -4:'4', -5:'5', -6:'6', -7:'7', -8:'8', 0:'N0', 1:'N1', 2:'N2', 3:'N3'}
    while True:
        if keyboard.is_pressed('q'):
            break
        winner = p.run(eval_genomes, 20)
        if winner.fitness >= sreda.kolvo:
            with open('data.pickle', 'wb') as f:
                pickle.dump(winner, f)
            visualize.draw_net(config, winner, True, node_names=node_names)
            break
        visualize.draw_net(config, winner, True, node_names=node_names)
    print('\nBest genome:\n{!s}'.format(winner))
    simul(winner, config)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)