from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from tel_API.keyboard.lexicon import LEXICON_RU, LEXICON_RU1


def works_chast() -> ReplyKeyboardMarkup:
    """Кнопки для кол-ва выводимых круизов"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard1 = KeyboardButton(LEXICON_RU['top'])
    keyboard.add(keyboard1)
    return keyboard

def search_you() -> ReplyKeyboardMarkup():
    """Кнопки для выбора статуса"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard1 = KeyboardButton(LEXICON_RU['ur'])
    keyboard2 = KeyboardButton(LEXICON_RU['chast'])
    keyboard.add(keyboard2,keyboard1)
    return keyboard

def works_ur() -> ReplyKeyboardMarkup:
    """Кнопки выбора видов работ"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard1 = KeyboardButton(LEXICON_RU['seti'])
    keyboard2 = KeyboardButton(LEXICON_RU['top'])
    keyboard.add(keyboard2, keyboard1)
    return keyboard

def search_you_ur_seti() -> ReplyKeyboardMarkup():
    """Кнопки для выбора юр лица сети"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard1 = KeyboardButton(LEXICON_RU['fio_prorab'])
    keyboard2 = KeyboardButton(LEXICON_RU['fio_ingener'])
    keyboard3 = KeyboardButton(LEXICON_RU['num_ras'])
    keyboard4 = KeyboardButton(LEXICON_RU['telephon'])
    keyboard5 = KeyboardButton(LEXICON_RU['next'])
    keyboard.add(keyboard1, keyboard2, keyboard3, keyboard4, keyboard5)
    return keyboard

def search_you_ur_top() -> ReplyKeyboardMarkup():
    """Кнопки для выбора юр лица топосъемка"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard1 = KeyboardButton(LEXICON_RU['name_object'])
    keyboard2 = KeyboardButton(LEXICON_RU['number_kadastr'])
    keyboard3 = KeyboardButton(LEXICON_RU['telephon'])
    keyboard4 = KeyboardButton(LEXICON_RU['next'])
    keyboard.add(keyboard1, keyboard2, keyboard3, keyboard4)
    return keyboard

def search_you_chast_top() -> ReplyKeyboardMarkup():
    """Кнопки для выбора частника  топосъемка"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard1 = KeyboardButton(LEXICON_RU['fio'])
    keyboard2 = KeyboardButton(LEXICON_RU['num_pasport'])
    keyboard3 = KeyboardButton(LEXICON_RU['data_pasport'])
    keyboard4 = KeyboardButton(LEXICON_RU['give_pasport'])
    keyboard5 = KeyboardButton(LEXICON_RU['adress_pr'])
    keyboard6 = KeyboardButton(LEXICON_RU['number_kadastr'])
    keyboard7 = KeyboardButton(LEXICON_RU['telephon'])
    keyboard8 = KeyboardButton(LEXICON_RU['next'])
    keyboard.add(keyboard1, keyboard2, keyboard3, keyboard4, keyboard5, keyboard6, keyboard7, keyboard8)
    return keyboard

def yes_or_no_button() -> ReplyKeyboardMarkup:
    """Кнопки 'Да' и 'Нет'"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard1 = KeyboardButton(LEXICON_RU['yes'])
    keyboard2 = KeyboardButton(LEXICON_RU['no'])
    keyboard.add(keyboard1, keyboard2)
    return keyboard

def search_one_button() -> ReplyKeyboardMarkup:
    """Кнопка 'Да'"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard1 = KeyboardButton(LEXICON_RU['number_kadastr'])
    keyboard.add(keyboard1)
    return keyboard


def delete_history() -> ReplyKeyboardMarkup:
    """Кнопка для очистки истории"""
    keyboard = ReplyKeyboardMarkup()
    keyboard.add((KeyboardButton("❌Очистить историю❌")))
    return keyboard

