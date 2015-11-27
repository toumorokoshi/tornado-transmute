import flask_transmute
import tornado.testing
import tornado.web
import tornado_transmute
import json


class TestApp(tornado.testing.AsyncHTTPTestCase):

    def get_app(self):
        return tornado.web.Application(_get_route_set())

    def test_foo(self):
        resp = self.fetch("/foo")
        assert resp.code == 200
        resp_json = json.loads(resp.body.decode("UTF-8"))
        assert resp_json.get("success")
        assert resp_json.get("result") == "Foo"


class ExampleHandler(tornado.web.RequestHandler):

    @tornado_transmute.handle_args
    @tornado_transmute.annotate({"resource": str, "multiplier": int})
    def get(self, resource, multiplier=None):
        pass
