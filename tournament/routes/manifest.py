import json
import tornado.web
import tornado.escape
import os
dir_path = os.path.dirname(os.path.realpath(__file__))


class LoadHandler(tornado.web.RequestHandler):

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
        submission_dir = os.path.join(dir_path, "..", "submissions", submission_id)
        manifest_file = os.path.join(submission_dir, "_manifest.json")

        try:
            with open(manifest_file, "r") as f:
                self.write({
                    "type": "OK",
                    "message": "Loaded the Manifest",
                    "data": json.load(f)
                })
        except Exception as e:
            self.set_status(500)
            self.write({
                "type": "INVALID_MANIFEST_DATA",
                "message": str(e)
            })
            self.finish()
            return

        self.finish()
        return


class SaveHandler(tornado.web.RequestHandler):

    def post(self):
        try:
            request_data = tornado.escape.json_decode(self.request.body)
            submission_id = request_data["submission_id"]
            manifest_data = request_data["data"]
        except Exception as e:
            self.set_status(500)
            self.write({
                "type": "INVALID_REQUEST_DATA",
                "message": e
            })
            self.finish()
            return

        if not self.validate_manifest(manifest_data):
            self.set_status(500)
            self.write({
                "type": "INVALID_MANIFEST_DATA",
                "message": None
            })
            self.finish()
            return

        submission_dir = os.path.join(dir_path, "..", "submissions", submission_id)
        manifest_file = os.path.join(submission_dir, "_manifest.json")

        try:
            with open(manifest_file, "w+") as file:
                file.write(json.dumps(manifest_data, indent=2, sort_keys=True))
        except Exception as e:
            self.write({
                "type": "INVALID_MANIFEST_DATA",
                "message": str(e)
            })

        self.write({
            "type": "OK",
            "message": "Manifest was saved"
        })
        self.finish()
        return

    def validate_manifest(self, data):
        # TODO
        return True
    get = post