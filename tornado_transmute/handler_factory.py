import tornado.web
import web_transmute


class HandlerFactory(object):
    """
    HandleFactory handles aggregating transmute functions
    into a set of handlers.
    """

    def __init__(self):
        self._handlers = {}

    def add_handler(self, path, transmute_func):
        if path not in self._handlers:
            self._handlers[path] = _create_handler()

        handler = self._handlers[path]

        _add_transmute_func_to_handler(transmute_func, handler)

    def get_handler_tuples(self):
        handlers = []
        for path, handler in self._handlers.items():
            handlers.append((path, handler))
        return handlers


def _create_handler():

    class Handler(tornado.web.RequestHandler):
        pass

    return Handler


def _add_transmute_func_to_handler(transmute_func, handler):
    handler_method = generate_handler_method(transmute_func)

    is_get = True

    for method in transmute_func.http_methods:
        is_get = False
        setattr(handler, method.lower(), handler_method)

    if is_get:
        setattr(handler, "get", handler_method)


def generate_handler_method(transmute_func):

    def method(self, *args):
        try:
            kwargs = _extract_args_get(self, transmute_func, args=args)
            result = transmute_func.raw_func(self, *args, **kwargs)
            self.set_header("Content-Type", "application/json")
            self.write({
                "success": True,
                "result": result
            })
        except Exception as e:
            if (transmute_func.error_exceptions and
               isinstance(e, transmute_func.error_exceptions)):
                self.write({
                    "success": False,
                    "details": str(e)
                })
            else:
                raise

    return method


def _extract_args_get(handler, transmute_func, args=None):
    kwargs = {}
    args = args or []
    # TODO: there needs to be a good strategy to parse out
    # positional arguments keyward arguments
    # (due to tornado accepting positional arguments matching regex.)
    index = len(args)
    for arg in transmute_func.argspec.args[index:]:
        args.append()

    for name, info in transmute_func.arguments.items():
        serializer = web_transmute.serializer[info.type]
        value = handler.get_query_argument(name, default=None)
        if value is not None:
            kwargs[name] = serializer.deserialize(value)
    return kwargs


def _extract_args_post(handler, transmute_func, args=None):
    kwargs = {}
    # TODO: there needs to be a good strategy to parse out
    # positional arguments keyward arguments
    # (due to tornado accepting positional arguments matching regex.)
    for name, info in transmute_func.arguments.items():
        serializer = web_transmute.serializer[info.type]
        value = handler.get_query_argument(name, default=None)
        if value is not None:
            kwargs[name] = serializer.deserialize(value)
    return kwargs


def _convert_to_args_kwargs(argspec):
    args, kwargs = [], {}
    attributes = (getattr(argspec, "args", []) +
                  getattr(argspec, "keywords", []))

    for i, name in enumerate(reversed(attributes)):
        if name == "self":
            continue

        if len(argspec.defaults) >= i:
            kwargs[name] = argspec.defaults[i]
        else:
            args.insert(0, name)

    return args, kwargs
