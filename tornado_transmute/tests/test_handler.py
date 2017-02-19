import tornado.testing
import tornado.web
import tornado_transmute
import json


def _create_app():
    app = tornado.web.Application([
        # one can use tornado_transmute's route function here.
        tornado_transmute.url("/foo/([^\/]+)", ExampleHandler),
    ])
    tornado_transmute.add_swagger(app, "/swagger.json", "/swagger")
    return app


class _SkipTestApp(tornado.testing.AsyncHTTPTestCase):

    def get_app(self):
        return tornado.web.Application([
            ("/foo/([^\/]+)", ExampleHandler),
        ])

    def test_foo(self):
        resp = self.fetch("/foo/bar")
        assert resp.code == 200
        resp_json = json.loads(resp.body.decode("UTF-8"))
        assert resp_json.get("success")
        assert resp_json.get("result") == 2

    def test_foo_queryparam(self):
        resp = self.fetch("/foo/bar?multiplier=2")
        assert resp.code == 200
        resp_json = json.loads(resp.body.decode("UTF-8"))
        assert resp_json.get("success")
        assert resp_json.get("result") == 4

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


class ExampleHandler(tornado.web.RequestHandler):

    # convert_handler can be called to convert a route to
    # a tornado handler.
    @tornado_transmute.convert_to_handler()
    @tornado_transmute.annotate({
        "resource": str, "multiplier": int,
        "return": int
    })
    @tornado.gen.coroutine
    def get(self, resource, multiplier=1):
        return 2 * multiplier

# tornado_transmute also provides a RouteSet, which can output tornado-compatible url objects.
# this provides a more flask-like approach, and handles combining routes which have the same path

route_set = tornado_transmute.RouteSet()

@tornado_transmute.route(route_set, paths="get")
def foo():
    pass

route_set.generate_urls()

if __name__ == "__main__":
    app = _create_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
