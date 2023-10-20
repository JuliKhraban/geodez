from pandas import DataFrame
from database.hangler_database import db_write, db_delete
from loader import bot
from database.common.models import History, db
from state.info import UserInfoState


def view_history(dict):
    db_write(db, History, dict)
    db.close()


@bot.message_handler(state=UserInfoState.clean_history)
def clean_history(message) -> None:
    k = 0
    bot.delete_state(message.from_user.id)
    for id in History.select().order_by(History.id.desc()):
        if k == 0:
            db_delete(db, History, id)
        k += 1

    bot.send_message(message.from_user.id, "История очищена")
    db.close()





