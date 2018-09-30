import json
import shutil

import tornado.web
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

class FileListHandler(tornado.web.RequestHandler):

    def get(self):

        # Verify that uploader id is set
        submission_id = None
        try:
            submission_id = str(self.get_argument("submission_id"))

            if len(submission_id) != 9:
                raise LookupError("Uploader ID should be the length of 9")
        except Exception as e:
            self.set_status(500)
            self.write(json.dumps({
                "type": "INVALID_SUBMISSION_ID",
                "message": str(e)
            }))
            self.finish()
            return

        # Construct uploader_project path
        uploader_project = os.path.join(dir_path, "..", "submissions", submission_id)

        if not os.path.exists(uploader_project):
            self.set_status(500)
            self.write(json.dumps({
                "type": "SUBMISSION_NOT_FOUND",
                "message": None
            }))
            return

        files = []
        for file in  os.listdir(uploader_project):
            files.append({
                "filename": file,
                "last_edited": os.path.getatime(os.path.join(uploader_project, file)),
                "size": os.path.getsize(os.path.join(uploader_project, file))
            })

        self.set_status(200)
        self.write({
            "type": "OK",
            "message": "Received submission file list",
            "data": files
        })
        return


class DeleteHandler(tornado.web.RequestHandler):

    def post(self):

        submission_id = str(self.get_argument("submission_id", default=None))
        delete_type = str(self.get_argument("delete_type", default="files"))
        if submission_id is None:
            self.set_status(500)
            self.write({
                "type": "INVALID_SUBMISSION_ID",
                "message": None
            })
            self.finish()
            return

        uploader_project = os.path.join(dir_path, "..", "submissions", submission_id)
        if delete_type == "files":
            for item in os.listdir(uploader_project):
                if item.endswith(".py"):
                    os.remove(os.path.join(uploader_project, item))
        elif delete_type == "submission":
            shutil.rmtree(uploader_project)


        self.write({
            "type": "SUBMISSION_DELETED",
            "message": None
        })
        self.finish()
    get = post

