from flask_script import Manager

from helloshopify import create_app
from helloshopify.extensions import db
from helloshopify import config


manager = Manager(create_app)

@manager.command
def run_debug():
    """run app in debug mode using adhoc ssl. 
    Make sure that in production you have valid certs.

    """

    app = create_app(config.DefaultConfig)
    app.run(debug=True, host='0.0.0.0', ssl_context='adhoc')

@manager.command
def initdb():
    """ Initialize database.

    """

    db.drop_all()
    db.create_all()
    db.session.commit()

if __name__ == "__main__":
    manager.run()
