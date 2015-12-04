from web_transmute import *
from web_transmute.function import TransmuteFunction
from .handler_factory import generate_handler_method


def convert_to_route(**options):

    def decorator(fn):
        transmute_func = TransmuteFunction(fn, **options)
        return generate_handler_method(transmute_func)

    return decorator
