from loader import bot
from telebot.custom_filters import StateFilter
from tel_API.utils.set_bot_commands import set_default_commands
from tel_API.handlers import handler, reguest

if __name__ == '__main__':
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    bot.infinity_polling(timeout=10, long_polling_timeout = 5)



