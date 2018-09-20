import gym
from axis_and_allies.game import Game
from axis_and_allies.nation import Nation
from axis_and_allies.modified_bot import NewBot
from axis_and_allies.modified_bot import NewBot2


"""
while True:
    if game.is_there_a_winner():
        break
    if not game.current_player.human:
        game.bot()
        print(game.turn)
    else:
        if game.phase == 0:
            game.phase_0()
        elif game.phase == 1:
            used = 0
            possible_unit_purchases = game.recruitable(game.purchase_units - used)
            # Here one should add some AI logic, that decides what if it should buy units (from possible_unit_purchases)
            # or simply skip to next phase.
            print(possible_unit_purchases)
            # In the example below, a unit type is randomly picked from the list of possible units.
            choice = r.randint(0, len(possible_unit_purchases) - 1)
            game.recruit_unit(choice)
            used += possible_unit_purchases[choice]
            # This procedure should be repeated until the AI decides it is enough, or it isn't possible to buy anymore.
            game.next_phase()

        elif game.phase == 2:
            # This is the phase that allows the AI to move units into enemy territory
            game.battles = []
            unit = game.movable[0]
            # Again here, the AI should have some logic for where to move the units.
            # In this example, the first moveable unit is moved to a random location.
            pos = unit.get_position()
            toTile = r.choice(game.map.board[pos[0]][pos[1]].neighbours)
            game.move_unit(game.map.board[pos[0]][pos[1]], toTile, 1, unit)
            # This procedure should be repeated until there are no more units to moved.
            game.next_phase()
        elif game.phase == 2.5:
            # This the phase where the battles is being executed.
            if len(game.battles) > 0:
                print("Do actions")
                results = game.do_battle(game.battles[0])
                attacker = results[0]
                defender = results[1]
            game.next_phase()
        elif game.phase == 3:
            # This is the same as phase two, just not allowed to move into unfriendly territory.
            # Again here the AI should make a decision, if it should move or not.
            unit = game.movable[0]
            pos = unit.get_position()
            possible = [tile for tile in game.map.board[pos[0]][pos[1]].neighbours if tile.owner == game.current_player]

            if len(possible) != 0:
                toTile = r.choice(possible)
                game.move_unit(game.map.board[pos[0]][pos[1]], toTile, 1, unit)

            game.next_phase()
        elif game.phase == 4:
            # Not implemented yet
            game.next_phase()
        elif game.phase == 5:
            # This is the phase where one places the units that is produced in phase 1.
            if game.current_player in game.purchases and game.deployable_places.__len__() > 0:
                tile = game.deployable_places[0]
                unit = game.purchases[game.current_player][0]
                game.purchases[game.current_player].remove(unit)
                tile.units.append(unit)
                unit.set_position(tile.cords)

            if game.is_there_a_winner():
                break
            else:
                game.reset_all_units()
                if not game.valid_board()[0]:
                    print("Not Valid mando")
                    print(game.map.board)
                game.next_phase()



"""


class AxisAndAllies4x4RandomAgent(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        bot = NewBot2(attack_threshold=0.1)
        bot2 = NewBot2(attack_threshold=0.35)
        germany = Nation(name='Germany', human=False, bot=bot)
        russia = Nation(name='Russia', human=False, bot=bot2)

        x, y = 4, 4

        self.game = Game(size=(4, 4), nations=[germany, russia])

    def __step__(self, action):

        # Here we need to handle the phases / logic
        pass
        """
        
        self._take_action(action)
        self.status = self.env.step()
        reward = self._get_reward()
        ob = self.env.getState()
        episode_over = self.status != hfo_py.IN_GAME
        """


        return s, r, t, {}

    def _reset(self):
        pass

    def _render(self, mode='human', close=False):
        pass

    def _take_action(self, action):
        pass

    def _get_reward(self):
        return 0