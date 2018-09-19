
import pygame
import numpy as np
from PIL import Image
from pygame.locals import *

from nation import Nation
from game import Game, GameManager
import new_bot as new_bots
from modified_bot import NewBot


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
    x, y = 8, 8

    germany = Nation(name='Germany', human=False)
    russia = Nation(name='Russia', human=False, difficulty="Easy")
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


def without_pauses():
    x, y = 6, 6
    from modified_bot import NewBot2

    bot = NewBot2(attack_threshold=0.1)
    bot2 = NewBot2(attack_threshold=0.35)
    germany = Nation(name='Germany', human=False, difficulty='new_bot', bot=bot)
    russia = Nation(name='Russia', human=False, difficulty="new_bot", bot=bot2)

    game = Game(size=(x, y), nations=[germany, russia])

    pygame.init()

    width, height = 1024, 768
    screen = pygame.display.set_mode((width, height))
    i = 0
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    while True:
        game.bot()
        if game.is_there_a_winner():
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


# with_pauses()
without_pauses()

