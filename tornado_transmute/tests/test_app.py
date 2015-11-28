import flask_transmute
import tornado.testing
import tornado.web
import tornado_transmute
import json


class TestApp(tornado.testing.AsyncHTTPTestCase):

    def get_app(self):
        return tornado.web.Application(_get_route_set())

    def x_test_foo(self):
        resp = self.fetch("/foo")
        assert resp.code == 200
        resp_json = json.loads(resp.body.decode("UTF-8"))
        assert resp_json.get("success")
        assert resp_json.get("result") == "Foo"


def _get_route_set():
    route_set = tornado_transmute.TornadoRouteSet()
    route_set.route_function("/foo", test_foo)
    route_set.route_function("/triple", triple)
    return route_set.generate_handlers()


def test_foo():
    return "Foo"


@flask_transmute.annotate({"triple": int, "return": int})
def triple(value):
    return value * 2
