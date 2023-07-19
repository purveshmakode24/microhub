from main import app, db
from flask_migrate import Migrate, upgrade, init, migrate as m
from flask.cli import FlaskGroup


migrate = Migrate(app, db)

cli = FlaskGroup(app)

"""
Commands:
1) python manager.py db_init
2) python manager.py db_migrate
3) python manager.py db_upgrade
"""

@cli.command("db_init")
def db_init():
    init()

@cli.command("db_migrate")
def db_migrate():
    m()

@cli.command("db_upgrade")
def db_upgrade():
    upgrade()


if __name__ == '__main__':
    cli()