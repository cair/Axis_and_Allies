import json

import tornado.web
import os
import importlib.util

from axis_and_allies.game import Game
from axis_and_allies.modified_bot import NewBot2, NewBot3
from axis_and_allies.nation import Nation

dir_path = os.path.dirname(os.path.realpath(__file__))
# jpqaw53r9


class TournamentHandler(tornado.web.RequestHandler):

    def get(self):

        submission_id = self.get_argument("submission_id", default=None)

        if submission_id is None:
            self.set_status(500)
            self.write({
                "type": "INVALID_SUBMISSION_ID",
                "message": None
            })
            self.finish()
            return

        data = self.run_tournament_for(submission_id)

        self.write({
            "type": "OK",
            "message": "Executed a tournament round!",
            "data": data
        })
        self.finish()

    def run_tournament_for(self, submission_id):
        bot_1 = self.load_submission(submission_id)
        opponents = [
            self.load_submission(x) for x in os.listdir(os.path.join(dir_path, "..", "submissions"))
        ]

        # Load Predefined bots
        opponents.append(NewBot2(0.10))
        opponents.append(NewBot3())

        # Create output buffer
        output = []
        # Run first series
        for bot_2 in opponents:
            output.append(self.run_game(bot_1=bot_1, bot_2=bot_2))
            output.append(self.run_game(bot_1=bot_2, bot_2=bot_1))

        return output

    def load_submission(self, submission_id):
        submission_path = os.path.join(dir_path, "..", "submissions", submission_id)
        manifest_data = json.load(open(os.path.join(submission_path, "_manifest.json"), "r"))

        entrypoint = os.path.join(submission_path, manifest_data["entrypoint"])
        entryclass = manifest_data["class_name"]
        entryclass_arguments = manifest_data["class_arguments"]

        spec = importlib.util.spec_from_file_location("%s.%s" % (submission_id, entryclass), entrypoint)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        bot_class = getattr(module, entryclass)
        bot_instance = bot_class(**entryclass_arguments)

        return bot_instance

    def run_game(self, bot_1, bot_2, n_games=6, w=6, h=6):
        germany = Nation(name=str(bot_1.__module__), bot=bot_1)
        russia = Nation(name=str(bot_2.__module__), bot=bot_2)
        results = {
            'bot_1': {'bot_name': str(bot_1.__module__), 'wins': 0, 'avg_rounds': 0} ,
            'bot_2': {'bot_name': str(bot_2.__module__), 'wins': 0, 'avg_rounds': 0}

        }

        for i in range(0, n_games):
            game = Game(size=(w, h), nations=[germany, russia])
            while True:
                game.bot()
                is_there_a_winner, winner = game.is_there_a_winner()
                if is_there_a_winner:
                    if winner == game.nations[0]:
                        results['bot_1']['wins'] +=1
                        results['bot_1']['avg_rounds'] += game.turn / n_games
                    elif winner == game.nations[1]:
                        results['bot_2']['wins'] += 1
                        results['bot_2']['avg_rounds'] += game.turn / n_games
                    break
        return results
