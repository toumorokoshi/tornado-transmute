import tornado.web


def url_spec(transmute_path, handler, *args, **kwargs):
    """
    convert the transmute_path
    to a tornado compatible regex,
    and return a tornado url object.
    """
    return tornado.web.URLSpec(
        _to_tornado_pattern(transmute_path),
        handler,
        *args, **kwargs
    )


def _to_tornado_pattern(transmute_path):
    """ convert a transmute path to
    a tornado pattern.
    """
    return (transmute_path
            .replace("{", "(P<")
            .replace("}", ">[^\/]+)"))
