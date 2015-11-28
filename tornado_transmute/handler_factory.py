import tornado.web


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

METHOD_MAP = {
    "creates": "PUT",
    "deletes": "delete",
    "updates": "POST",
}


def _add_transmute_func_to_handler(transmute_func, handler):
    handler_method = generate_handler_method(transmute_func)

    is_get = True
    for attr, method in METHOD_MAP.items():
        if getattr(transmute_func, attr, False):
            is_get = False
            setattr(handler, attr.lower(), handler_method)

    if is_get:
        setattr(handler, "get", handler_method)


def generate_handler_method(transmute_func):

    def method(self, *args):
        try:
            kwargs = _extract_args(self, transmute_func, args=args)
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


def _extract_args(handler, transmute_func, args=None):
    kwargs = {}
    return kwargs
