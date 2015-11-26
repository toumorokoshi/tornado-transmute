import tornado_transmute
import tornado.testing
import tornado.web


class TestApp(tornado.testing.AsyncHTTPTestCase):

    def get_app(self):
        return tornado.web.Application(_get_route_set())

    def test_app(self):
        response = self.fetch("/")
        assert response.code == 200


def _get_route_set():
    route_set = tornado_transmute.TornadoRouteSet()
    route_set.route_function("/", test_foo)


def test_foo():
    return "Foo"
