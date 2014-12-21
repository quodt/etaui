from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import (
    Authenticated,
    Allow,
)

from sqlalchemy import create_engine

from model import DBSession, Base


class Root(object):
    __acl__ = [
        (Allow, Authenticated, 'view'),
        (Allow, 'group:public', 'view'),
    ]

    def __init__(self, request):
        self.request = request


def app_factory(global_config, **settings):
    """Setup the main application for paste

    This must be setup as the paste.app_factory in the egg entry-points.
    """
    authn_policy = AuthTktAuthenticationPolicy(
        settings['auth.secret'],
        # 30 days age for the session cookie
        max_age=60 * 60 * 24 * 30,
        reissue_time=60 * 60 * 24,
    )
    authz_policy = ACLAuthorizationPolicy()

    config = Configurator(
        settings=settings,
        authentication_policy=authn_policy,
        authorization_policy=authz_policy,
        root_factory=Root,
        autocommit=True,
    )

    config.include('eta.service', route_prefix='/api/v1')
    config.scan('eta.service')
    config.add_static_view('', '../static')
    init_db(config)
    return config.make_wsgi_app()


def init_db(config):
    settings = config.get_settings()
    path = settings.get('db.path', 'var/eta.db')
    engine = create_engine("sqlite:///%s" % path)
    Base.metadata.create_all(engine)
    DBSession.configure(bind=engine)
