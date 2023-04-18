from tornado.testing import AsyncHTTPTestCase
import tornado
from src.functional import get_fib
from src import fib


class TestFibApp(AsyncHTTPTestCase):
    def __init__(self,  # type: ignore[no-untyped-def]
                 *args,  # type: ignore[no-untyped-def]
                 **kwargs) -> None:  # type: ignore[no-untyped-def]
        super().__init__(*args, **kwargs)
        self.fibs = {
            0: 0,
            1: 1,
            2: 1,
            3: 2,
            19: 4181,
            250: 7896325826131730509282738943634332893686268675876375}

    def get_app(self) -> tornado.web.Application:
        return fib.make_app()

    def test_homepage(self) -> None:
        response = self.fetch('/')
        msg = 'homepage fail'
        self.assertEqual(response.code, 200, msg)
        self.assertEqual(response.body,
                         b'Go to "/your_number" for example: ' +
                         b'<a href="/100">link</a>',
                         msg)

    def test_fib_calculation(self) -> None:
        for n, v in self.fibs.items():
            self.assertEqual(get_fib(n), v, 'fib calculation error')

    def test_fib_response(self) -> None:
        for n, v in self.fibs.items():
            response = self.fetch('/' + str(n))
            self.assertEqual(int(response.body), v, 'fib response error')
