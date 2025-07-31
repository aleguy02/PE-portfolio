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
        database = mydb


def init_db():
    try:
        if mydb.is_closed():
            mydb.connect()
        mydb.create_tables([TimelinePost])
    except Exception as e:
        print(f"Database initialization error: {e}")


def close_db():
    if not mydb.is_closed():
        mydb.close()
