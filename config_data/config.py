from environs import Env

env = Env()
env.read_env()
BOT_TOKEN = env('BOT_TOKEN')

DEFAULT_COMMANDS = (
    ('start', "Запустить бота, начать сначала"),
    ('help', "Вывести список команд"),
    ('stop', "До свидания!"),

)
