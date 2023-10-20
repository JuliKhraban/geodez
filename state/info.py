from telebot.handler_backends import State, StatesGroup

class UserInfoState(StatesGroup):
    def __init__(self) -> None:
        super().__init__()
        self.data = {}

    wait_state = State()  # да/нет
    name_state = State()  # юр лицо/частник
    select_work = State()  # сети/топосъемка
    select_work_chast = State()
    name_object = State()
    name = State()
    phone_number = State()
    phone_number1 = State()
    phone_number2 = State()
    fio_prorab = State()
    fio_ingineer = State()
    search_number = State()
    number_pasport = State()
    dat_pasport = State()
    give_pasport = State()
    clean_history = State()
    number_order = State()
    object_name = State() #название объекта
    number_kadastr = State()
    number_kadastr1 = State()
    clean_histor = State()
    name_state_new = State()
    adress_live = State()
    back = State()
    back1 = State()
    back2 = State()
    last_state = State()

    def get_state(self, chat_id, user_id):
        if self.data.get(chat_id):
            if self.data[chat_id].get(user_id):
                return self.data[chat_id][user_id]['state']

        return None

    def reset_data(self, chat_id, user_id):
        if self.data.get(chat_id):
            if self.data[chat_id].get(user_id):
                self.data[chat_id][user_id]['data'] = {}
                return True
        return False



