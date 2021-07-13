import pyowm
import telebot
import sqlite3

from pyowm.utils.config import get_default_config

config_dict = get_default_config()
config_dict['language'] = 'ru'

owm = pyowm.OWM('4ecd09d1d2a7375673797f77c4b84899', config_dict)
mgr = owm.weather_manager()

bot = telebot.TeleBot('1885853306:AAFRLTNaO9QBjTC1SneFY3Tzz_LoMxs2EF0')


@bot.message_handler(content_types=['text'])
def send_echo(message):
    connect = sqlite3.connect('pogoda_selec.db')

    cursor = connect.cursor()

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER,
                city TEXT
            )
        """)

    connect.commit()
    print(message)

    # add values
    user_id = message.from_user.id
    text_1 = message.text
    name_1 = message.from_user.first_name
    last_1 = message.from_user.last_name
    username_1 = message.from_user.username

    cursor.execute('INSERT INTO users VALUES(?, ?, ?, ?, ?);', (user_id, text_1, name_1, last_1, username_1))

    connect.commit()


    # while True:
    try:
        observation = mgr.weather_at_place(message.text)
        w = observation.weather
        # bot.reply_to(message, message.text)
        # break

        # except NotFoundError:
        # answer = 'Город не найден'

        temp = w.temperature('celsius')["temp"]

        answer = 'В городе ' + message.text + ' сейчас ' + w.detailed_status + '\n'
        answer += 'Температура сейчас в районе ' + str(temp) + '\n\n'

        if temp < -10:
            answer += 'Одевайтесь тепло'
        elif temp < 0:
            answer += 'Одевайся как хочешь'
        elif temp < 10:
            answer += 'Ходи голышом'
        elif temp < 20:
            answer += 'Не выходи из дома'
        elif temp > 20:
            answer += 'Шутка. Можешь выйти'

        bot.send_message(message.from_user.id, answer)
        hack = 'Пользователь ' + message.from_user.username + ' отправил мне запрос: ' + message.text
        bot.send_message(596834788, hack)
    except:
        answer = 'Введи город правильно и попробуй еще раз'
        bot.send_message(message.from_user.id, answer)
        hack = 'Пользователь ' + message.from_user.username + ' отправил мне запрос: ' + message.text
        bot.send_message(596834788, hack)


bot.polling(none_stop=True)
