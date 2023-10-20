from typing import Dict, List, TypeVar
from peewee import ModelSelect

from database.common.models import ModelBase
from database.common.models import db

T = TypeVar("T")


def _store_date(db: db, model: T, data: Dict) -> None:
    with db.atomic():
        response = model.insert_many(data).execute()
    return response

def _delete_date(db: db, model: T, id) -> None:
    with db.atomic():
        response = model.delete_instance(id)
    return response

def _retrieve_all_data(db: db, model: T, *columns: ModelBase) -> ModelSelect:
    with db.atomic():
        response = model.select(*columns)
    return response


class CRUDInteface():
    @staticmethod
    def create():
        return _store_date

    @staticmethod
    def read():
        return _retrieve_all_data

    @staticmethod
    def delete():
        return _delete_date