import json

import tornado.web
import logging
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
import importlib.util
from axis_and_allies.game import Game
from axis_and_allies.nation import Nation
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