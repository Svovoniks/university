import telebot
from telebot import types
import datetime
import psycopg2

token = ""
bot = telebot.TeleBot(token)

commands = [
    telebot.types.BotCommand('start', 'Start the bot'),
    telebot.types.BotCommand('help', 'Show the help message'),
    telebot.types.BotCommand('week', 'Show current week parity'),
    telebot.types.BotCommand('mtuci', 'Show link to the university website')]

bot.set_my_commands(commands)

conn = psycopg2.connect(database="bot_db",
                        user="",
                        password="",
                        host="",
                        port="")

cursor = conn.cursor()

subj_template = '''-------
{2} - {3}
<{0}>
{1}
{4}'''

day_template = '''
<{week_day}>
____________
{0}
-------
____________
'''

weekdays = ['Понедельник',
          'Вторник',
          'Среда',
          'Четверг',
          'Пятница']

def week_parity():
    return datetime.datetime.now().isocalendar()[1]%2

def get_one_day(day, incr):
    
    cursor.execute("SELECT s.name, t.room_numb, t.start_time, t.end_time, p.full_name FROM bot.timetable t, bot.subject s, bot.teacher p WHERE t.day='{}' AND t.week={} AND s.id=p.subject AND s.id=t.subject".format(day, (week_parity()+incr)%2))
    full_day = ''
    for i in sorted(list(cursor.fetchall()), key=lambda a: a[2]):
        full_day+=subj_template.format(*i)+'\n'
    return day_template.format(full_day[:-1], week_day=day)

def get_week(msg, incr):
    for i in weekdays:
        msg+=get_one_day(i.upper(), incr=incr)
    return msg

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    short_days = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', ]
    keyboard.row(*short_days)
    keyboard.row('Текущая неделя', 'Следующая неделя')

    bot.send_message(
        message.chat.id,
        'Привет! Я бот с расписанием группы БВТ2204',
        reply_markup=keyboard)
    help_message(message)

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id,
     '''Я умею показывать расписание на определённый день недели с помощью команд: 
Пн
Вт
Ср
Чт
Пт

Tакже могу сказать расписание на текущую и следующую недели с помощью соответствующих команд

А ещё могу сказать какая сейчас неделя: чётная или нет, и даже дать ссылку на сайт университета''')

@bot.message_handler(commands=['week'])
def week_message(message):
    if week_parity():
        bot.send_message(message.chat.id, 'Сейчас нечётная неделя')
    else:
        bot.send_message(message.chat.id, 'Сейчас чётная неделя')

@bot.message_handler(commands=['mtuci'])
def mtutci_message(message):
    bot.send_message(message.chat.id, 'Официальный сайт mtuci: https://mtuci.ru/')

@bot.message_handler(content_types=['text'])
def answer(message):
    resp='Извините, я Вас не понял'

    if message.text in ls:
        tpl = ls[message.text]
        resp = tpl[0](*tpl[1:])
    bot.send_message(
        message.chat.id, resp)


ls = {'Пн': (get_one_day, 'ПОНЕДЕЛЬНИК', 0),
          'Вт': (get_one_day, 'ВТОРНИК', 0),
          'Ср': (get_one_day, 'СРЕДА', 0),
          'Чт': (get_one_day, 'ЧЕТВЕРГ', 0),
          'Пт': (get_one_day, 'ПЯТНИЦА', 0),
          'Текущая неделя': (get_week, 'Расписание на текущую неделю',0),
          'Следующая неделя':(get_week, 'Расписание на следующую недели', 1)}

bot.infinity_polling()

