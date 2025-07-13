import os, datetime
from peewee import *

## Part 1
mydb = MySQLDatabase(
    os.getenv("MYSQL_DATABASE"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST"),
    port=3306,
)

## Part 2
# Define a model (table) for storing timeline posts in the database.
# This uses Peewee, an ORM (Object Relational Mapper) for Python, which allows you to interact with databases using Python classes instead of SQL queries.


class TimelinePost(Model):  # A model is a representation or view of a table
    # Each attribute below represents a column in the database table.

    name = CharField()  # CharField is used for short text strings.
    email = CharField()  # Also a short text string.
    content = TextField()  # TextField is used for longer text.
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        # The Meta class is used to configure model-specific settings.
        database = mydb  # Specifies which database this model will use.


mydb.connect()
# this command is idempotent, we can run it as many times as we want but only one table will be created
mydb.create_tables([TimelinePost])
