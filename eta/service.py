from lovely.pyrest.rest import RestService, rpcmethod_view
from model import Entry


@RestService('status')
class UserService(object):

    def __init__(self, request):
        self.request = request

    @rpcmethod_view(http_cache=0)
    def get(self, **kwargs):
        """Return current status
        """
        e = Entry.latest()
        if e:
            return e.as_dict()
        return {}


def includeme(config):
    config.add_route('status', '/status', static=True)
