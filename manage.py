from app import app, db
from flask_migrate import migrate
from flask.cli import FlaskGroup
from app import app
cli = FlaskGroup(app)


if __name__ == "__main__":
    cli()