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

    async def get(self):

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

    def run_game(self, bot_1, bot_2):
        germany = Nation(name=str(bot_1.__module__), bot=bot_1)
        russia = Nation(name=str(bot_2.__module__), bot=bot_2)
        results = {}
        number_of_rounds = 100
        for i in range(0, number_of_rounds):
            game = Game(size=(6, 6), nations=[germany, russia])
            while True:
                game.bot()
                is_there_a_winner, winner = game.is_there_a_winner()
                if is_there_a_winner:
                    if 'winner' not in results:
                        results['winner'] = {}
                        results['avg_rounds'] = {}

                    if winner not in results['winner']:
                        results['winner'][winner.name] = 0
                        results['avg_rounds'][winner.name] = 0

                    results['winner'][winner.name] +=1
                    results['avg_rounds'][winner.name] += game.turn/number_of_rounds
                    break
        return results
