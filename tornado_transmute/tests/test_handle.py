import tornado.testing
import tornado.web
import tornado_transmute
import json

# tornado_transmute also provides a RouteSet, which can output tornado-compatible url objects.
# this provides a more flask-like approach, and handles combining routes which have the same path


@tornado_transmute.describe(paths="/foo/{multiplier}")
@tornado_transmute.annotate({"multiplier": int, "return": int})
def get(self, multiplier):
    return 2 * multiplier


class TestApp(tornado.testing.AsyncHTTPTestCase):

    def get_app(self):
        route_set = tornado_transmute.RouteSet()
        route_set.add(get)
        app = tornado.web.Application(route_set.generate_url_specs())
        # tornado_transmute.add_swagger(app, "/swagger.json", "/swagger")
        return app

    def test_foo(self):
        resp = self.fetch("/foo/1")
        assert resp.code == 200
        resp_json = json.loads(resp.body.decode("UTF-8"))
        assert resp_json == 2

    def test_swagger_json(self):
        resp = self.fetch("/swagger.json")
        assert resp.code == 200
        resp_json = json.loads(resp.body.decode("UTF-8"))
        assert "get" in resp_json["paths"]["/foo/([^\/]+)$"]
        assert resp_json["swagger"] == "2.0"
        assert resp_json["info"] == {
            "title": "swagger", "version": "1.0"
        }

    def test_swagger_body(self):
        resp = self.fetch("/swagger")
        assert resp.code == 200
        body = resp.body.decode("UTF-8")
        assert "swagger-section" in body
