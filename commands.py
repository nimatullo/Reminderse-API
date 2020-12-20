import click
from flask.cli import with_appcontext

from flasktest import db
from models import Users, Links, Text, Category

@click.command(name="create_tables")
@with_appcontext
def create_tables():
    db.create_all()