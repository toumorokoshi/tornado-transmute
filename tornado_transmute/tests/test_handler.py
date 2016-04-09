import tornado.testing
import tornado.web
import tornado_transmute
import json


class TestApp(tornado.testing.AsyncHTTPTestCase):

    def get_app(self):
        app = tornado.web.Application([
            ("/foo/([^\/]+)", ExampleHandler)
        ])
        swagger_handler = tornado_transmute.generate_swagger_json_handler(app)
        app.add_handlers(".*", [("/swagger.json", swagger_handler)])
        return app

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
        assert resp_json == {
            "paths": {},
            "swagger": "2.0",
            "info": {
                "title": "swagger",
                "version": "1.0"
            }
        }


class ExampleHandler(tornado.web.RequestHandler):

    @tornado_transmute.to_route()
    @tornado_transmute.annotate({
        "resource": str, "multiplier": int,
        "return": int
    })
    def get(self, resource, multiplier=1):
        return 2 * multiplier
