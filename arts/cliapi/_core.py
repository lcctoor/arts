import logging
from tornado.web import Application, RequestHandler
from tornado.httputil import HTTPServerRequest as Request
from typing import Callable


logging.getLogger("tornado.access").setLevel(logging.ERROR)
logging.getLogger("tornado.application").setLevel(logging.ERROR)
logging.getLogger("tornado.general").setLevel(logging.ERROR)


def server(get: Callable[[Request], str]=None, post: Callable[[Request], str]=None, port: int=8888, address: str=None, *_, **kwargs):
    get_handle, post_handle = get, post
    
    class MiniHandler(RequestHandler):
        if get_handle:
            async def get(self):
                self.set_header("Access-Control-Allow-Origin", "*")
                self.write(get_handle(self.request))
        
        if post_handle:
            async def post(self):
                self.set_header("Access-Control-Allow-Origin", "*")
                self.write(post_handle(self.request))

    app = Application([(r"/.*", MiniHandler)])
    app.listen(port, address=address, **kwargs)
    print(f"cliapi server is running.")
    return app