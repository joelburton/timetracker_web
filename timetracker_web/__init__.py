"""Time tracker web app."""

from pyramid.config import Configurator
from pyramid_zodbconn import get_connection

from .models import appmaker


def root_factory(request):
    """Get root of database."""

    conn = get_connection(request)
    return appmaker(conn.root())


def main(global_config, **settings):
    """This function returns a Pyramid WSGI application. """

    config = Configurator(root_factory=root_factory, settings=settings)

    config.include('pyramid_jinja2')

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('deform_static', 'deform:static/')

    config.scan()

    return config.make_wsgi_app()
