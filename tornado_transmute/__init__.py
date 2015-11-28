import tornado.web
from flask_transmute.routeset import RouteSet
from .handler_factory import HandlerFactory
from flask_transmute.function import TransmuteFunction
from .handler_factory import generate_handler_method
from flask_transmute import annotate


class TornadoRouteSet(RouteSet):

    def __init__(self, *args, **kwargs):
        super(TornadoRouteSet, self).__init__(*args, **kwargs)

    def generate_handlers(self):
        handler_factory = HandlerFactory()
        for route_config in self._routes:
            handler_factory.add_handler(
                route_config.path, route_config.transmute_func
            )

        return handler_factory.get_handler_tuples()


def _create_handler(transmute_func):

    class Handler(tornado.web.RequestHandler):

        def get(self):
            self.write("Hello, " + transmute_func.description)

    return Handler


def convert_to_route(**options):

    def decorator(fn):
        transmute_func = TransmuteFunction(fn, **options)
        return generate_handler_method(transmute_func)

    return decorator
