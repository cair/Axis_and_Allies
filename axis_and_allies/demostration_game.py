import pygame
import numpy as np
from PIL import Image
from pygame.locals import *
from pprint import pprint

from axis_and_allies.game import Game, GameManager
from axis_and_allies.nation import Nation
from axis_and_allies.modified_bot import NewBot
from axis_and_allies.bot import Bot
from axis_and_allies.modified_bot import NewBot2


def translate_to_array(board, x, y, game):
    new_board = np.zeros((x, y, 3), dtype=np.uint8)
    global_max = game.find_global_max()
    for w in board:
        for h in w:
            if h.owner.name == 'Germany':
                new_board[h.cords[0]][h.cords[1]] = np.asarray([0, 45 + int((80 * h.units.__len__()) / global_max), 0],
                                                               dtype=np.uint8)
            elif h.owner.name == 'Russia':
                new_board[h.cords[0]][h.cords[1]] = np.asarray(
                    [150 + (int(105 * h.units.__len__()) / global_max), 0, 0],
                    dtype=np.uint8)

    return new_board


def with_pauses():
    x, y = 5, 5

    germany = Nation(name='Germany')
    russia = Nation(name='Russia')
    game = Game(size=(x, y), nations=[germany, russia])

    game_manager = GameManager()

    pygame.init()

    width, height = 1024, 768
    screen = pygame.display.set_mode((width, height))
    update = True
    first = True
    while True:
        if update:
            screen.fill(0)
            data = translate_to_array(game.map.board, x, y, game)
            img = Image.fromarray(data, 'RGB')
            img = img.resize((1024, 768))
            # img.show()
            img = pygame.surfarray.make_surface(np.array(img))
            screen.blit(pygame.transform.rotate(img, 90), (0, 0))
            pygame.display.flip()
            update = False

        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == K_RETURN:
                    while True:
                        if first:
                            game_manager.add_previous(game)
                            first = False
                        game.bot()
                        print(game.phase, game.turn)
                        update = True
                        if game.phase == 0:
                            first = True
                            break
                        elif game.is_there_a_winner():
                            break
                if event.key == K_BACKSPACE:
                    game = game_manager.go_back()
                    update = True


def without_graphics():
    x, y = 6, 6
    bot = Bot()
    bot2 = Bot()
    bot = NewBot2(attack_threshold=0.12)
    bot2 = NewBot2(attack_threshold=0.12)
    germany = Nation(name='Germany', bot=bot)
    russia = Nation(name='Russia', bot=bot2)

    results = {}
    number_of_rounds = 100
    for i in range(0, number_of_rounds):
        game = Game(size=(x, y), nations=[germany, russia])
        while True:
            game.calculate_values()
            game.bot()
            is_there_a_winner, winner = game.is_there_a_winner()
            if is_there_a_winner:
                if 'winner' not in results:
                    results['winner'] = {}
                    results['avg_rounds'] = {}

                if winner not in results['winner']:
                    results['winner'][winner] = 0
                    results['avg_rounds'][winner] = 0

                results['winner'][winner] +=1
                results['avg_rounds'][winner] += game.turn/number_of_rounds
                #pprint(game.history)
                break
    print(results)



def without_pauses():
    x, y = 6, 6
    bot = Bot()
    bot2 = Bot()
    bot = NewBot2(attack_threshold=0.10)
    #bot2 = NewBot2(attack_threshold=0.20)#NewBot3()
    germany = Nation(name='Germany', bot=bot)
    russia = Nation(name='Russia', bot=bot2)

    game = Game(size=(x, y), nations=[germany, russia])

    pygame.init()

    width, height = 1024, 768
    screen = pygame.display.set_mode((width, height))
    i = 0
    while True:
        game.bot()
        is_there_a_winner, winner = game.is_there_a_winner()
        if is_there_a_winner:
            print(winner)
            screen.fill(0)
            data = translate_to_array(game.map.board, x, y, game)
            img = Image.fromarray(data, 'RGB')
            img = img.resize((1024, 768))
            img = pygame.surfarray.make_surface(np.array(img))
            screen.blit(pygame.transform.rotate(img, 90), (0, 0))
            pygame.display.flip()
            pygame.time.wait(10)
            break

        if i % 15 == 0:
            screen.fill(0)
            data = translate_to_array(game.map.board, x, y, game)
            img = Image.fromarray(data, 'RGB')
            img = img.resize((1024, 768))
            img = pygame.surfarray.make_surface(np.array(img))

            screen.blit(pygame.transform.rotate(img, 90), (0, 0))
            pygame.display.flip()
            pygame.time.wait(50)
        i += 1


#with_pauses()
#without_pauses()
without_graphics()
