from database.utils.CRUD import CRUDInteface
from database.common.models import db, History

db.connect()


with db:
    tables = [History]
    if not db.table_exists(table for table in tables):
        db.create_tables(tables)
print('Done')


crud = CRUDInteface()


if __name__ == "__main__":
    CRUDInteface()