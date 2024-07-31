import logging, re
from tornado.web import Application, RequestHandler
from tornado.httputil import HTTPServerRequest
from typing import Callable
from arts.cooltypes import Coolstr


logging.getLogger("tornado.access").setLevel(logging.ERROR)
logging.getLogger("tornado.application").setLevel(logging.ERROR)
logging.getLogger("tornado.general").setLevel(logging.ERROR)


class Pathplus:
    def __init__(self, parts: tuple):
        self.parts = parts
    
    def __bool__(self): return bool(self.parts)

    def __len__(self): return len(self.parts)

    def __str__(self): return ''.join(self.parts)

    def asstr(self): return str(self)

    def __iter__(self):
        for x in self.parts:
            yield self.__class__((x,))
    
    def __getitem__(self, _index_or_slice):
        try:
            r = self.parts[_index_or_slice]
        except IndexError:
            return self.__class__(tuple())
        if type(r) is tuple:
            return self.__class__(r)
        else:
            return self.__class__((r,))
    
    @property
    def name(self) -> str|None:
        if self:
            return self.parts[-1][1:]
        else:
            return None

    def search(self, _pattern: str):
        return re.search(_pattern, str(self))
    
    def findall(self, _pattern: str):
        return re.findall(_pattern, str(self))
    
    def __eq__(self, _obj):
        if type(_obj) is self.__class__:
            _obj = str(_obj)
        return str(self) == _obj


class Requestplus:
    def __init__(self, handler: RequestHandler, _tornado_request: HTTPServerRequest):
        self.handler = handler
        self._tornado_request = _tornado_request
    
    path: Pathplus

    def __getattr__(self, _name):
        if _name == 'path':
            self.path = Pathplus(tuple(re.findall(r'/[^/]*', self._tornado_request.path)))
            return self.path
        return getattr(self._tornado_request, _name)


# 此类用于代码提示
class Request(HTTPServerRequest):
    handler: RequestHandler
    path: Pathplus


async def method_base(self: RequestHandler, method: Callable[[Request], str|bytes]):
    self.set_header("Access-Control-Allow-Origin", "*")
    r = await method(Requestplus(self, self.request))
    if type(r) is tuple:
        if mime_type := Coolstr(suffix := f".{r[1]}").get_mime_types()[0]:
            self.set_header("Content-Type", mime_type)
        self.write(r[0])
    else:
        if mime_type := Coolstr(self.request.path).get_mime_types()[0]:
            is_text = mime_type.startswith('text/')
            if (is_text and type(r) is str) or (not is_text and type(r) is bytes):
                self.set_header("Content-Type", mime_type)
        self.write(r)


def server(*_,
           get: Callable[[Request], str|bytes]=None,
           post: Callable[[Request], str|bytes]=None,
           port: int=8888,
           address: str=None,
           debug=False,
           **kwargs
):
    get_ = get
    post_ = post
    
    class MiniHandler(RequestHandler):
        if get_:
            async def get(self):
                await method_base(self, get_)
        
        if post_:
            async def post(self):
                await method_base(self, post_)

    app = Application([(r"/.*", MiniHandler)], debug=debug)
    app.listen(port, address=address, **kwargs)
    print(f"cliapi server is running.")
    return app