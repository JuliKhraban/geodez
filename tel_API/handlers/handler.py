from telebot.types import Message, ReplyKeyboardRemove
from state.info import UserInfoState
from tel_API.handlers.history import view_history, clean_history
from tel_API.handlers.new_keybord import search_you_chast_top1, clean, search_you_ur_seti1, \
    search_you_ur_top1
from tel_API.keyboard.lexicon import LEXICON_RU1
from tel_API.keyboard.reply import yes_or_no_button, search_you, works_ur, works_chast, search_you_ur_seti, \
    search_you_ur_top, search_you_chast_top, LEXICON_RU, search_one_button
from tel_API.handlers.reguest import search_number
from loader import bot
from config_data.config import DEFAULT_COMMANDS

@bot.message_handler(commands=['start'])
def bot_start(message: Message):
    clean()
    bot.reply_to(message, f'\U0001F609 Привет! {message.from_user.first_name}, я новый сотрудник ИП Храбан Б.А.\n'
                          f'У меня испытательный срок, поэтому я могу делать ошибки, но я буду очень стараться вам помочь.\n'
                          f'Для вызова меню-подсказки, нажимайте "/"\n'
                          f'Пока, только нажимайте на кнопки. Давайте начнем!\U0001F447', reply_markup=yes_or_no_button())
    answer = message
    bot.set_state(message.from_user.id, UserInfoState.wait_state, message.chat.id)

@bot.message_handler(commands=['help'])
def bot_help(message: Message):
    text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS]
    bot.reply_to(message, '\n'.join(text))

@bot.message_handler(commands=['stop'])
def bot_stop(message: Message):
    bot.reply_to(message, f'До свидания! {message.from_user.first_name}, чтобы начать заново, нажмите на /start')
    bot.delete_state(message.from_user.id)

@bot.message_handler(state=UserInfoState.wait_state)
def start_answer(answer: Message) -> None:
    if answer.text == LEXICON_RU['yes']:
        with bot.retrieve_data(answer.from_user.id, answer.chat.id) as data:
            data["command"] = answer.text
            data["user_id"] = answer.from_user.id
        bot.send_message(answer.from_user.id, f"{answer.from_user.first_name}, делайте выбор: \U0001F447", reply_markup=search_you())
        bot.set_state(answer.from_user.id, UserInfoState.name_state, answer.chat.id)
    elif answer.text == LEXICON_RU['no']:
        bot.send_message(answer.from_user.id, f'{answer.from_user.first_name}, до свидания! Чтобы начать заново, нажмите на /start')
        bot.delete_state(answer.from_user.id)
    else:
        bot.send_message(answer.from_user.id, f'{answer.from_user.first_name}, нажмите "Да" или "Нет"! \U0001F447', reply_markup=yes_or_no_button())
        bot.set_state(answer.from_user.id, UserInfoState.wait_state, answer.chat.id)

@bot.message_handler(state=UserInfoState.name_state)
def get_state(message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name_state'] = message.text
    if message.text == LEXICON_RU['ur']:
        bot.send_message(message.from_user.id, f'{message.from_user.first_name}, выбирайте вид работ, нажимайте кнопку:\U0001F447', reply_markup=works_ur())
        bot.set_state(message.from_user.id, UserInfoState.select_work, message.chat.id)
    elif message.text == LEXICON_RU['chast']:
        bot.send_message(message.from_user.id, f'{message.from_user.first_name}, Теперь нажимайте "Топосъемка":\U0001F447"', reply_markup=works_chast())
        bot.set_state(message.from_user.id, UserInfoState.select_work_chast, message.chat.id)
    else:
        bot.send_message(message.from_user.id, f'{message.from_user.first_name}, делайте свой выбор:\U0001F447', reply_markup=search_you())
        bot.set_state(message.from_user.id, UserInfoState.name_state, message.chat.id)


@bot.message_handler(state=UserInfoState.select_work)
def choice_works_ur(message) -> None:

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name_work'] = message.text
    if message.text == LEXICON_RU['seti']:
        bot.send_message(message.from_user.id, f"Вы выбрали: {message.text}. Работаем дальше!\n"
                                            f"Мне необходима следующая информация.\n"
                                            f"Жмите на кнопку 'ФИО прораба' и вводите нужный текст. ", reply_markup=search_you_ur_seti())
        bot.register_next_step_handler(message, fio_prorab)
    elif message.text ==LEXICON_RU['top']:
        bot.send_message(message.from_user.id, f"Вы выбрали: {message.text}. Работаем дальше!\n"
                                            f"Мне необходима следующая информация,\n"
                                            f"Жмите на кнопку 'Название объекта' и вводите нужный текст. ", reply_markup=search_you_ur_top())
        bot.register_next_step_handler(message, name_object)
    else:
        bot.send_message(message.from_user.id, f'{message.from_user.first_name}, выбирайте вид работ, нажимайте кнопку:\U0001F447"',
                             reply_markup=works_ur())
        bot.set_state(message.from_user.id, UserInfoState.select_work, message.chat.id)

"""Собираю данные юридическое лицо - сети"""
@bot.message_handler(state=UserInfoState.back)
def back_menu(message):
    fio_prorab(message)

def fio_prorab(message) -> None:
    if message.text == LEXICON_RU['fio_prorab']:
        bot.send_message(message.from_user.id, f"Напишите ФИО прораба: ", reply_markup=ReplyKeyboardRemove())
        bot.set_state(message.from_user.id, UserInfoState.fio_prorab, message.chat.id)

    elif message.text ==LEXICON_RU['fio_ingener']:
        bot.send_message(message.from_user.id, f"Напишите ФИО инженера: ", reply_markup=ReplyKeyboardRemove())
        bot.set_state(message.from_user.id, UserInfoState.fio_ingineer, message.chat.id)

    elif message.text == LEXICON_RU['num_ras']:
        bot.send_message(message.from_user.id, f"Напишите номер ордера на раскопки: ", reply_markup=ReplyKeyboardRemove())
        bot.set_state(message.from_user.id, UserInfoState.number_order, message.chat.id)

    elif message.text == LEXICON_RU['telephon']:
        bot.send_message(message.from_user.id, f"Напишите свой номер телефона: ", reply_markup=ReplyKeyboardRemove())
        bot.set_state(message.from_user.id, UserInfoState.phone_number, message.chat.id)

    elif message.text == LEXICON_RU['next']:
        bot.send_message(message.from_user.id, f"Последний рывок! ")
        bot.set_state(message.from_user.id, UserInfoState.last_state, message.chat.id)
        get_info(message)

    else:
        bot.send_message(message.from_user.id, f"Нажмите, пожалуйста, на кнопку:", reply_markup=search_you_ur_seti1(message))
        bot.set_state(message.from_user.id, UserInfoState.back, message.chat.id)


@bot.message_handler(state=UserInfoState.fio_prorab)
def fio_prorab1(message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name_prorab'] = message.text
    bot.reply_to(message, f"Проверяйте ФИО прораба: {message.text}")
    bot.send_message(message.chat.id, 'Выберите следующий пункт меню:', reply_markup=search_you_ur_seti1(LEXICON_RU1['fio_prorab']))
    bot.set_state(message.from_user.id, UserInfoState.back, message.chat.id)


@bot.message_handler(state=UserInfoState.fio_ingineer)
def fio_inginer(message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name_ingineer'] = message.text
    bot.reply_to(message, f"Проверяйте ФИО инженера: {message.text}")
    bot.send_message(message.chat.id, 'Выберите следующий пункт меню:', reply_markup=search_you_ur_seti1(LEXICON_RU1['fio_ingener']))
    bot.set_state(message.from_user.id, UserInfoState.back, message.chat.id)


@bot.message_handler(state=UserInfoState.number_order)
def number_order(message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['number_order'] = message.text
    bot.reply_to(message, f"Проверяйте номер ордера: {message.text}")
    bot.send_message(message.chat.id, 'Выберите следующий пункт меню:', reply_markup=search_you_ur_seti1(LEXICON_RU1['num_ras']))
    bot.set_state(message.from_user.id, UserInfoState.back, message.chat.id)


@bot.message_handler(state=UserInfoState.phone_number)
def number_phone(message) -> None:
    bot.reply_to(message, f"Проверяйте номер телефона: {message.text}")
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['number_phone'] = message.text
    bot.send_message(message.chat.id, 'Выберите последний пункт меню:', reply_markup=search_you_ur_seti1(LEXICON_RU1['telephon']))
    bot.set_state(message.from_user.id, UserInfoState.back, message.chat.id)

"""Собираю данные юридическое лицо - топосъемка"""
clean()
@bot.message_handler(state=UserInfoState.back1)
def back_menu(message):
    name_object(message)

def name_object(message) -> None:
    if message.text == LEXICON_RU['name_object']:
        bot.send_message(message.from_user.id, f"Укажите название объекта: ", reply_markup=ReplyKeyboardRemove())
        bot.set_state(message.from_user.id, UserInfoState.object_name, message.chat.id)

    elif message.text == LEXICON_RU['number_kadastr']:
        bot.send_message(message.from_user.id, f"Теперь напишите кадастровый номер (должно быть 18 цифр!!!):", reply_markup=ReplyKeyboardRemove())
        bot.set_state(message.from_user.id, UserInfoState.number_kadastr, message.chat.id)

    elif message.text == LEXICON_RU['telephon']:
        bot.send_message(message.from_user.id, f"Напишите свой номер телефона: ", reply_markup=ReplyKeyboardRemove())
        bot.set_state(message.from_user.id, UserInfoState.phone_number1, message.chat.id)

    elif message.text == LEXICON_RU['next']:
        bot.send_message(message.from_user.id, f"Последний рывок! ")
        get_info(message)

    else:
        bot.send_message(message.from_user.id, f"Нажмите, пожалуйста, на кнопку:", reply_markup=search_you_ur_top1(message.text))
        bot.set_state(message.from_user.id, UserInfoState.back1, message.chat.id)


@bot.message_handler(state=UserInfoState.object_name)
def name_object1(message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name_object'] = message.text
    bot.reply_to(message, f"Проверяйте название объекта: {message.text}")
    bot.send_message(message.chat.id, 'Выберите следующий пункт меню:', reply_markup=search_you_ur_top1(LEXICON_RU['name_object']))
    bot.set_state(message.from_user.id, UserInfoState.back1, message.chat.id)

@bot.message_handler(state=UserInfoState.number_kadastr)
def number_kadastr(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['kadastr_number'] = message.text
    if len(data['kadastr_number']) == 18:
        bot.reply_to(message, f"В вашем номере 18 цифр, главное, чтобы они были верными!: {message.text}")
        bot.send_message(message.chat.id, 'Выберите следующий пункт меню:', reply_markup=search_you_ur_top1(LEXICON_RU['number_kadastr']))
    else:
        bot.reply_to(message, f"Не верно,попробуйте еще раз : {message.text}")
        bot.send_message(message.chat.id, 'Нажмите на кнопку "Кадастровый номер":',
                         reply_markup=search_one_button())
    bot.set_state(message.from_user.id, UserInfoState.back1, message.chat.id)

@bot.message_handler(state=UserInfoState.phone_number1)
def number_phone(message) -> None:
    bot.reply_to(message, f"Проверяйте телефон: {message.text}")
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['number_phone'] = message.text
    bot.send_message(message.chat.id, 'Выберите последний пункт меню:', reply_markup=search_you_ur_top1(LEXICON_RU['telephon']))
    bot.set_state(message.from_user.id, UserInfoState.back1, message.chat.id)

"""Частнички"""
clean()
@bot.message_handler(state=UserInfoState.select_work_chast)
def choice_works_chast(message)-> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name_work'] = message.text
    if message.text == LEXICON_RU['top']:
        bot.send_message(message.from_user.id, f"Мне необходима следующая информация.\n"
                                               f"Жмите на кнопку 'Ваше ФИО' и вводите нужный текст. ", reply_markup=search_you_chast_top())
        bot.register_next_step_handler(message, get_fio)
    else:
        bot.send_message(message.from_user.id, f"Жмите на топосъемку!!!", reply_markup=works_chast())
        bot.set_state(message.from_user.id, UserInfoState.select_work_chast, message.chat.id)

clean()

@bot.message_handler(state=UserInfoState.back2)
def back_menu(message):
    get_fio(message)

def get_fio(message) -> None:
        if message.text == LEXICON_RU['fio']:
            bot.send_message(message.from_user.id, f"Укажите ваше ФИО: ", reply_markup=ReplyKeyboardRemove())
            bot.set_state(message.from_user.id, UserInfoState.name, message.chat.id)

        elif message.text == LEXICON_RU['num_pasport']:
            bot.send_message(message.from_user.id, f"Теперь напишите серию и номер паспорта:", reply_markup=ReplyKeyboardRemove())
            bot.set_state(message.from_user.id, UserInfoState.number_pasport, message.chat.id)

        elif message.text == LEXICON_RU['data_pasport']:
            bot.send_message(message.from_user.id, f"Теперь напишите дату выдачи паспорта:", reply_markup=ReplyKeyboardRemove())
            bot.set_state(message.from_user.id, UserInfoState.dat_pasport, message.chat.id)

        elif message.text == LEXICON_RU['give_pasport']:
            bot.send_message(message.from_user.id, f"Теперь напишите кем выдан паспорт:", reply_markup=ReplyKeyboardRemove())
            bot.set_state(message.from_user.id, UserInfoState.give_pasport, message.chat.id)

        elif message.text == LEXICON_RU['adress_pr']:
            bot.send_message(message.from_user.id, f"Теперь напишите ваш адрес  прописки:", reply_markup=ReplyKeyboardRemove())
            bot.set_state(message.from_user.id, UserInfoState.adress_live, message.chat.id)

        elif message.text == LEXICON_RU['number_kadastr']:
            bot.send_message(message.from_user.id, f"Теперь напишите кадастровый номер вашего участка (должно быть 18 цифр!!!):",
                             reply_markup=ReplyKeyboardRemove())
            bot.set_state(message.from_user.id, UserInfoState.number_kadastr1, message.chat.id)

        elif message.text == LEXICON_RU['telephon']:
            bot.send_message(message.from_user.id, f"Напишите свой телефон в произвольном формате:", reply_markup=ReplyKeyboardRemove())
            bot.set_state(message.from_user.id, UserInfoState.phone_number2, message.chat.id)

        elif message.text == LEXICON_RU['next']:
            bot.send_message(message.from_user.id, f"Последний рывок! ")
            get_info(message)
        else:
            bot.send_message(message.from_user.id, f"Нажмите, пожалуйста, на кнопку:", reply_markup=search_you_chast_top1(message.text))
            bot.set_state(message.from_user.id, UserInfoState.back2, message.chat.id)



@bot.message_handler(state=UserInfoState.name)
def get_fio1(message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    bot.reply_to(message, f"Проверяйте: {message.text}")
    bot.send_message(message.chat.id, 'Выберите следующий пункт меню:', reply_markup=search_you_chast_top1(LEXICON_RU['fio']))
    bot.set_state(message.from_user.id, UserInfoState.back2, message.chat.id)


@bot.message_handler(state=UserInfoState.number_pasport)
def get_pasport_number(message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['pasport_number'] = message.text
    bot.reply_to(message, f"Проверяйте серию и номер паспорта: {message.text}")
    bot.send_message(message.chat.id, 'Выберите следующий пункт меню:', reply_markup=search_you_chast_top1(LEXICON_RU['num_pasport']))
    bot.set_state(message.from_user.id, UserInfoState.back2, message.chat.id)


@bot.message_handler(state=UserInfoState.dat_pasport)
def get_pasport_data(message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['pasport_data'] = message.text
    bot.reply_to(message, f"Проверяйте дату выдачи паспорта: {message.text}")
    bot.send_message(message.chat.id, 'Выберите следующий пункт меню:', reply_markup=search_you_chast_top1(LEXICON_RU['data_pasport']))
    bot.set_state(message.from_user.id, UserInfoState.back2, message.chat.id)


@bot.message_handler(state=UserInfoState.give_pasport)
def get_pasport_give(message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['pasport_give'] = message.text
    bot.reply_to(message, f"Проверяйте кем паспорт выдан: {message.text}")
    bot.send_message(message.chat.id, 'Выберите следующий пункт меню:', reply_markup=search_you_chast_top1(LEXICON_RU['give_pasport']))
    bot.set_state(message.from_user.id, UserInfoState.back2, message.chat.id)


@bot.message_handler(state=UserInfoState.adress_live)
def adress_live(message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['adress_live'] = message.text
    bot.reply_to(message, f"Проверяйте адрес прописки: {message.text}")
    bot.send_message(message.chat.id, 'Выберите следующий пункт меню:', reply_markup=search_you_chast_top1(LEXICON_RU['adress_pr']))
    bot.set_state(message.from_user.id, UserInfoState.back2, message.chat.id)

@bot.message_handler(state=UserInfoState.phone_number2)
def number_phone2(message) -> None:
    bot.reply_to(message, f"Проверяйте телефон: {message.text}")
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['number_phone'] = message.text
    bot.send_message(message.chat.id, 'Выберите следующий пункт меню:', reply_markup=search_you_chast_top1(LEXICON_RU['telephon']))
    bot.set_state(message.from_user.id, UserInfoState.back2, message.chat.id)

@bot.message_handler(state=UserInfoState.number_kadastr1)
def number_kadastr1(message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['kadastr_number'] = message.text
        if len(data['kadastr_number']) == 18:
            bot.reply_to(message, f"В вашем номере 18 цифр, главное, чтобы они были верными!: {message.text}")
            bot.send_message(message.chat.id, 'Выберите следующий пункт меню:', reply_markup=search_you_chast_top1(LEXICON_RU['number_kadastr']))
        else:
            bot.reply_to(message, f"Не верно,попробуйте еще раз : {message.text}")
            bot.send_message(message.chat.id, 'Нажмите на кнопку "Кадастровый номер":', reply_markup=search_one_button())
    bot.set_state(message.from_user.id, UserInfoState.back2, message.chat.id)

#@bot.message_handler(state=UserInfoState.last_state)
def get_info(message: Message) -> None:
    bot.send_message(message.from_user.id, "Вы указали следующие параметры (ждем...): ", reply_markup=ReplyKeyboardRemove())
    try:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            if data['name_state'] == LEXICON_RU['ur']:
                if data['name_work'] == LEXICON_RU['seti']:
                    text = f"ВЫ: {data['name_state']}\n"\
                       f"Разновидность работ : {data['name_work']}\n"\
                       f"ФИО прораба: {data['name_prorab']}\n"\
                       f"ФИО инженера: {data['name_ingineer']}\n" \
                       f"Номер ордера на раскопки: {data['number_order']}\n" \
                       f"Ваш контактный телефон: {data['number_phone']}\n"
                    dict = {'name': data['name_state'],
                            'name_work': data['name_work'],
                            'name_object': "",
                             'name_prorab':data['name_prorab'],
                             'name_ingineer': data['name_ingineer'],
                             'number_order': data['number_order'],
                             'number_kadastr': "",
                             'telephone': data['number_phone'],
                             'you_name': "",
                             'number_pasport': "",
                             'data_pasport': "",
                             'give_pasport': "",
                             'adress': "",
                             'adress_live': ""
                             }
                    bot.send_message(message.from_user.id, text)
                    bot.set_state(message.from_user.id, UserInfoState.clean_history, message.chat.id)

                    view_history(dict)

                    bot.send_message(message.from_user.id, 'Все верно? Отправляем эту информацию геодезисту?', reply_markup=yes_or_no_button())
                    bot.set_state(message.from_user.id, UserInfoState.name_state_new, message.chat.id)

                elif data['name_work'] == LEXICON_RU['top']:
                    text = f"ВЫ: {data['name_state']}\n"\
                        f"Разновидность работ : {data['name_work']}\n"\
                        f"Название объекта: {data['name_object']}\n"\
                        f"Кадастровый номер: {data['kadastr_number']}\n"\
                        f"Нужны реквизиты компании (можно  фото в вайбер или телеграмм) или пришлите  их мне на электронную почту: 6589653@tyt.by\n"\
                        f"Ваш контактный телефон: {data['number_phone']}\n"\
                        f"Адрес объекта: {search_number(message, data['kadastr_number'])}\n"
                    dict = {'name': data['name_state'],
                            'name_work': data['name_work'],
                            'name_object': data['name_object'],
                            'name_prorab': "",
                            'name_ingineer': "",
                            'number_kadastr': data['kadastr_number'],
                            'number_order': "",
                            'telephone': data['number_phone'],
                            'you_name': "",
                            'number_pasport': "",
                            'data_pasport': "",
                            'give_pasport': "",
                            'adress': "",
                            'adress_live': ""
                            }
                    bot.send_message(message.from_user.id, text)
                    bot.set_state(message.from_user.id, UserInfoState.clean_history, message.chat.id)
                    view_history(dict)

                    bot.send_message(message.from_user.id, 'Все верно? Отправляем эту информацию геодезисту?', reply_markup=yes_or_no_button())
                    bot.set_state(message.from_user.id, UserInfoState.name_state_new, message.chat.id)
            else:
                text = f"ВЫ: {data['name_state']}\n"\
                    f"Разновидность работ : {data['name_work']}\n"\
                    f"Ваше ФИО : {data['name']}\n" \
                    f"Серия и номер паспорта : {data['pasport_number']}\n" \
                    f"Дата выдачи : {data['pasport_data']}\n" \
                    f"Кем выдан : {data['pasport_give']}\n" \
                    f"Кадастровый номер: {data['kadastr_number']}\n"\
                    f"Адрес объекта: {search_number(message, data['kadastr_number'])}"\
                    f"\nВаш контактный телефон: {data['number_phone']}\n"\
                    f"Адрес прописки: {data['adress_live']}\n"

                dict = {'name': data['name_state'],
                        'name_work': data['name_work'],
                        'name_object': "",
                        'name_prorab': "",
                        'name_ingineer': "",
                        'number_order': "",
                        'you_name': data['name'],
                        'number_pasport': data['pasport_number'],
                        'data_pasport': data['pasport_data'],
                        'give_pasport': data['pasport_give'],
                        'number_kadastr': data['kadastr_number'],
                        'telephone': data['number_phone'],
                        'adress': '',
                        'adress_live': {data['adress_live']}
                        }
                bot.send_message(message.from_user.id, text)
                bot.set_state(message.from_user.id, UserInfoState.clean_history, message.chat.id)

                view_history(dict)

                bot.send_message(message.from_user.id, f'Все верно? Отправляем эту информацию геодезисту?', reply_markup=yes_or_no_button())
                bot.set_state(message.from_user.id, UserInfoState.name_state_new, message.chat.id)
    except:
        bot.send_message(message.from_user.id, f"\U0001F614 Вы нажали не на все кнопки, придется заполнить заново, нажимайте на /start", reply_markup=ReplyKeyboardRemove())
        clean()


@bot.message_handler(state=UserInfoState.name_state_new)
def end_answer(message: Message) -> None:
    if message.text == LEXICON_RU['yes']:
        bot.send_message(message.from_user.id, f"{message.from_user.first_name},\U0001F64F спасибо! Геодезист вам перезвонит, до свидания!",
                         reply_markup=ReplyKeyboardRemove())
        clean()


    else:
        bot.send_message(message.from_user.id, f'{message.from_user.first_name}, до свидания!',  reply_markup=ReplyKeyboardRemove())
        bot.set_state(message.from_user.id, UserInfoState.clean_history, message.chat.id)
        clean_history(message)
        clean()



