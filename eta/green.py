from gevent.pywsgi import WSGIServer, WSGIHandler


class LoggingWSGIHandler(WSGIHandler):

    def log_request(self):
        # do not log each request
        pass


def server_factory(global_conf, host, port):
    """Provide the WSGI server for paste

    This must be setup as the paste.server_factory in the egg entry-points.
    """
    port = int(port)

    def serve(app):
        def wafapp(environ, start_response):
            environ["wsgi.url_scheme"] = environ.get("HTTP_X_FORWARDED_PROTO",
                                                     "http")
            return app(environ, start_response)

        WSGIServer(
            (host, port),
            wafapp,
            handler_class=LoggingWSGIHandler,
        ).serve_forever()
    return serve

