import tornado.web
import logging
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
import importlib.util
from axis_and_allies.game import Game
from axis_and_allies.nation import Nation
from axis_and_allies.new_bot import Bot


class UploadHandler(tornado.web.RequestHandler):

    def post(self):

        for data in self.request.files["qqfile"]:
            filename = data["filename"]
            body = data["body"]

            bot_path = self.save_bot(filename, body)
            bot = self.load_bot(bot_path)


    get = post


    def save_bot(self, filename, body):
        full_filepath = os.path.join(dir_path, filename)
        with open(full_filepath, "wb+") as file:
            file.write(body)



    def load_bot(self, bot_path):
        spec = importlib.util.spec_from_file_location("module.name", bot_path)
        print(spec) # https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path

    def validate_submission(self):

        bot = Bot()
        bot2 = Bot()
        germany = Nation(name='Germany', human=False, difficulty='new_bot', bot=bot)
        russia = Nation(name='Russia', human=False, difficulty="new_bot", bot=bot2)
        results = {}
        number_of_rounds = 100
        for i in range(0, number_of_rounds):
            game = Game(size=(6, 6), nations=[germany, russia])
            while True:
                game.bot()
                if game.is_there_a_winner():
                    if 'winner' not in results:
                        results['winner'] = {}
                        results['avg_rounds'] = {}

                    if game.current_player not in results['winner']:
                        results['winner'][game.current_player] = 0
                        results['avg_rounds'][game.current_player] = 0

                    results['winner'][game.current_player] +=1
                    results['avg_rounds'][game.current_player] += game.turn/number_of_rounds
                    break
        print(results)
