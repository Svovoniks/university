import asyncio
import tornado.web
from src.functional import get_fib


class MainHandler(tornado.web.RequestHandler):
    def get(self) -> None:
        self.write('Go to "/your_number" for example: <a href="/100">link</a>')


class NumberHandler(tornado.web.RequestHandler):
    def get(self, number: int) -> None:
        self.write(str(get_fib(int(number))))


def make_app() -> tornado.web.Application:
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/(\d+)", NumberHandler)
    ])


async def main() -> None:
    app = make_app()
    app.listen(8888)
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
