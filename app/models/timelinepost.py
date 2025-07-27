import os
import datetime
from peewee import *


if os.getenv("TESTING") == "true":
    print("Running in testing mode")
    mydb = SqliteDatabase("file:memory:?mode=memory&cache=shared", uri=True)
else:
    mydb = MySQLDatabase(
        os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306,
    )


class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        # The Meta class is used to configure model-specific settings.
        database = mydb  # Specifies which database this model will use.


def init_db():
    """
    Initialize database connection and create tables
    """
    try:
        if mydb.is_closed():
            mydb.connect()

        # this command is idempotent, we can run it as many times as we want but only one table will be created
        mydb.create_tables([TimelinePost])
    except Exception as e:
        print(f"Database initialization error: {e}")
        # In testing or development without MySQL, we can continue without database connection
