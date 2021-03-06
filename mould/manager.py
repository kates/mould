import os
import subprocess
import errno

from flask import Flask
from flask.ext.script import Manager, Shell

import config
from mould.app import create_app
from mould.gunicorn_app import GunicornApp
from mould.utils import touch
from mould.utils import blueprint_template
from mould.migration import Migration

app = create_app(Flask(config.APP_NAME))
manager = Manager(app)

@manager.command
def server(port=5000):
    """Run gunicorn server"""
    options = {
        "bind": "0.0.0.0:%s" % port,
        "workers": 4,
        }
    gunicorn_app = GunicornApp(options, app)
    gunicorn_app.run()


@manager.command
def test():
    """Run tests"""
    import unittest
    suite = unittest.TestLoader()\
                .discover("tests", pattern="*_test.py")
    unittest.TextTestRunner(verbosity=config.TEST_VERBOSITY).run(suite)


@manager.command
def alembic():
    """Initialize alembic"""
    migration = Migration(app)
    migration.init()


@manager.command
def migrate(direction):
    """Migrate db revision"""
    migration = Migration(app)
    migration.migrate(direction)


@manager.command
def migration(message):
    """Create migration file"""
    migration = Migration(app)
    migration.migration(message)


@manager.command
def blueprint(name, path=None, templates=None):
    """create blueprint structure"""
    templates = templates or "templates"
    path = path or name
    blueprint_template(name, templates)


@manager.shell
def make_shell_context():
    return dict(app=app)

