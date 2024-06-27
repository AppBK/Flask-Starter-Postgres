from flask.cli import AppGroup
from .users import seed_users, undo_users

# from app.models.db import db, environment, SCHEMA

# Creates a seed group to hold our commands
# So we can type `flask seed --help`
seed_commands = AppGroup('seed')


# Creates the `flask seed all` command
@seed_commands.command('all')
def seed():
    # We will want to unseed before re-seeding so that we do not run into unique constraint errors.
    # Your seed undo commands here. Note that they should be run in opposite order from seeding
    undo_users()

    # your seed commands here.
    seed_users()


# Creates the `flask seed undo` command
@seed_commands.command('undo')
def undo():
    # Add other undo functions here. Again, unseeding should be done in opposite order from the seeding
    undo_users()
