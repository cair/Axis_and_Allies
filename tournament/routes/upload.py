import json

import tornado.web
import logging
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
import importlib.util
from axis_and_allies.game import Game
from axis_and_allies.nation import Nation
from axis_and_allies.new_bot import Bot
import json

class UploadHandler(tornado.web.RequestHandler):

    def post(self):
        submission_id = self.get_body_argument("submission_id", default=None, strip=False)

        if submission_id is None:
            self.set_status(500)
            self.write(json.dumps({
                "type": "INVALID_SUBMISSION_ID",
                "message": None
            }))
            self.finish()
            return

        uploader_dir = os.path.join(dir_path, "..", "submissions", submission_id)
        if not os.path.exists(uploader_dir):
            os.mkdir(uploader_dir)

            manifest_template = json.load(open(os.path.join(dir_path, "..", "manifest_template.json"), "r"))
            with open(os.path.join(uploader_dir, "_manifest.json"), "w+") as f:
                f.write(json.dumps(manifest_template))

        for data in self.request.files["qqfile"]:
            filename = data["filename"]
            body = data["body"]

            bot_path = self.save_file(os.path.join(uploader_dir, filename), body)
            #bot = self.load_bot(bot_path)

        self.set_status(200)
        self.write({
            "type": "OK",
            "message": "Files were successfully uploaded!",
            "success": True
        })
        self.finish()
    get = post

    def save_file(self, file_path, body):

        with open(file_path, "wb+") as file:
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
