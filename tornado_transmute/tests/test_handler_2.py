import tornado.testing
import tornado.web
import tornado_transmute
import json


class ExampleHandler(tornado.web.RequestHandler):

    # convert_handler can be called to convert a route to
    # a tornado handler.
    @tornado_transmute.convert_to_handler()
    @tornado_transmute.annotate({
        "resource": str, "multiplier": int,
        "return": int
    })
    @tornado.gen.coroutine
    def get(self, multiplier):
        return 2 * multiplier


class TestApp(tornado.testing.AsyncHTTPTestCase):

    def get_app(self):
        app = tornado.web.Application([
            # one can use tornado_transmute's route function here.
            tornado_transmute.url("/foo/{multiplier}", ExampleHandler),
        ])
        tornado_transmute.add_swagger(app, "/swagger.json", "/swagger")
        return app

    def test_foo(self):
        resp = self.fetch("/foo/1")
        assert resp.code == 200
        resp_json = json.loads(resp.body.decode("UTF-8"))
        assert resp_json.get("success")
        assert resp_json.get("result") == 2
