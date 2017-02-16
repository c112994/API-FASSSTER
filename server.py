import tornado.ioloop
import tornado.httpserver
import tornado.web
import os
import base64
from tornado import autoreload

from handlers.ApiHandler import ApiHandler

settings = {
            "debug": True,
            }

application = tornado.web.Application([
    (r"/api/gender", ApiHandler, dict(methodname='gender')),
    (r"/api/bmi", ApiHandler, dict(methodname='bmi')),
], **settings)

if __name__ == "__main__":
    application.listen(7777)
    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.start()