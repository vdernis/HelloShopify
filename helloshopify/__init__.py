from flask import Flask

from .config import DefaultConfig
from .shopify_bp import shopify_bp
from .extensions import db


__all__ = ['create_app']

DEFAULT_BLUEPRINTS = (
    shopify_bp,
)


def create_app(config=None, blueprints=None):
    """Create Flask app.

    """

    if blueprints is None:
        blueprints = DEFAULT_BLUEPRINTS

    app = Flask(__name__)
    configure_app(app, config)
    configure_blueprints(app, blueprints)
    configure_extensions(app)

    return app

def configure_app(app, config=None):
    """ Configure application.

    """
    
    app.config.from_object(DefaultConfig)

def configure_extensions(app):
    """ Configure extensions.

    """

    db.init_app(app)

def configure_blueprints(app, blueprints):
    """ Configure blueprints in views.

    """

    for blueprint in blueprints:
        app.register_blueprint(blueprint)