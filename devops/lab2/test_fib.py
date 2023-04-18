import fib
from fib import get_fib
from tornado.testing import AsyncHTTPTestCase
import unittest

class TestfFbApp(AsyncHTTPTestCase):
    def __init__(self, a):
        super().__init__(a)
        self.fibs = {0:0, 1:1, 2:1, 3:2, 19:4181, 250:7896325826131730509282738943634332893686268675876375}

    def get_app(self):
        return fib.make_app()

    def test_homepage(self):
        response = self.fetch('/')
        msg = 'homepage fail'
        self.assertEqual(response.code, 200, msg)
        self.assertEqual(response.body, b'Go to "/your_number" for example: <a href="/100">link</a>', msg)

    def test_fib_calculation(self):
        for n, v in self.fibs.items():
            self.assertEqual(get_fib(n), v, 'fib calculation error')

    def test_fib_response(self):
        for n, v in self.fibs.items():
            response = self.fetch('/'+str(n))
            self.assertEqual(int(response.body), v, 'fib response error')

unittest.main()