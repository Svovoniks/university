import asyncio
import tornado.web
import decimal

def get_fib(n):
    decimal.getcontext().prec = 10000

    root_5 = decimal.Decimal(5).sqrt()
    phi = ((1 + root_5) / 2)

    a = ((phi ** n) - ((-phi) ** -n)) / root_5

    return round(a)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Go to "/your_number" for example: <a href="/100">link</a>')

class NumberHandler(tornado.web.RequestHandler):
    def get(self, number):
        self.write(str(get_fib(int(number))))

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/(\d+)", NumberHandler)
    ])

async def main():
    app = make_app()
    app.listen(8888)
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())