from datetime import datetime
from peewee import *

db = SqliteDatabase('my_database.db')

class ModelBase(Model):
    created_at = DateField(default=datetime.now())

    class Meta():
        database = db

class History(ModelBase):
    name = CharField()
    name_work = CharField()
    name_object = TextField(null=False)
    name_prorab = CharField(null=False)
    name_ingineer = CharField(null=False)
    number_order = CharField(null=False)
    number_kadastr = CharField(null=False)
    telephone = CharField()
    you_name = CharField(null=False)
    number_pasport = CharField(null=False)
    data_pasport = CharField(null=False)
    give_pasport = CharField(null=False)
    adress = TextField(null=False)
    adress_live = TextField(null=False)