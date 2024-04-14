from peewee import *

db = SqliteDatabase('database.db')


class Player(Model):
    id = AutoField(unique=True)
    name = AnyField(null=True)
    score = AnyField(null=True)

    class Meta:
        database = db


Player.create_table()