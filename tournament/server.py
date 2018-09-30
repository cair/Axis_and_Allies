import tornado.ioloop
import tornado.web
import os

from tournament.routes import manifest, submission, upload, tournament

dir_path = os.path.dirname(os.path.realpath(__file__))


def setup_data_structure():

    tree = [
        os.path.join(dir_path, "submissions"),
        os.path.join(dir_path, "replays"),
        os.path.join(dir_path, "stats")
    ]

    for node in tree:
        if not os.path.exists(node):
            os.mkdir(node)


if __name__ == "__main__":
    setup_data_structure()

    app = tornado.web.Application([
        (r"/api/submission/file_list", submission.FileListHandler),
        (r"/api/submission/upload/", upload.UploadHandler),
        (r"/api/submission/delete", submission.DeleteHandler),
        (r"/api/manifest/save", manifest.SaveHandler),
        (r"/api/manifest/load", manifest.LoadHandler),
        (r"/api/tournament/run", tournament.TournamentHandler),
        (r"/(.*)", tornado.web.StaticFileHandler, {'path': os.path.join(dir_path, "www",), "default_filename": "index.html"}),
    ])
    app.listen(8889)
    tornado.ioloop.IOLoop.current().start()



