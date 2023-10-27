import telebot
from sidedatas import bot_token
from telebot import types
import random
from sidedatas import classes


bot = telebot.TeleBot(bot_token)


def list_of_data(any_class):
    pages = []
    with open(f"{any_class}.html", 'r') as file:
        for row in file:
            pages.append(row.rstrip())
    return pages


def list_of_gt(any_class):
    gtpages = []
    with open(f"{any_class}-gt.html", 'r') as file:
        for row in file:
            gtpages.append(row.rstrip())
    return gtpages


def combine_lists(list1, list2):
    res = dict(zip(list1, list2))
    return res


@bot.message_handler(commands=['start'])
def hello(message):
    bot.send_message(message.chat.id, 'Добрый день, напишите /classes что посмотреть полный список классов')


@bot.message_handler(commands=['classes'])
def get_classes(message):
    bot.send_message(message.chat.id,  '/' + '\n/'.join(classes) + '\n' + 'Выберите один из классов')


@bot.message_handler(content_types=['text'])
def get_class(message):
    if message.text[1:] in classes:
        msg = bot.send_message(message.chat.id,  'Отлично! Теперь тыкните /build или введите вручную для получения'
                                           ' рандомного билда этого класса')
        global class_in_url
        class_in_url = message.text[1:]
        bot.register_next_step_handler(msg, button)
    else:
        bot.send_message(message.chat.id, 'Неправильно ввели имя класса, попробуйте заново')


def get_final_list(stroka_klassa: str):
    data = list_of_data(stroka_klassa)
    gt = list_of_gt(stroka_klassa)
    final_list = combine_lists(data, gt)
    random_build = random.choice(list(final_list.items()))
    return random_build


@bot.message_handler(commands=['build'])
def button(message):
    markup = types.InlineKeyboardMarkup()
    item_forum = types.InlineKeyboardButton(text='Forum', callback_data='forumlink')
    item_gt = types.InlineKeyboardButton(text='GrimTools', callback_data='gtlink')

    markup.add(item_forum, item_gt)
    bot.send_message(message.chat.id, 'Куда желаете перейти?', reply_markup=markup)
    global value
    value = get_final_list(class_in_url)
    markup1 = types.InlineKeyboardMarkup()
    next_build = types.InlineKeyboardButton(text="Другой билд", callback_data='back')

    markup1.add(next_build)
    bot.send_message(message.chat.id, 'Другой билд?', reply_markup=markup1)


@bot.callback_query_handler(func=lambda call: True)
def answer_forum(call):
    if call.data == 'forumlink':
        bot.send_message(call.message.chat.id, value[0])
    elif call.data == 'gtlink':
        bot.send_message(call.message.chat.id, f'{value[1]} Одна из версий этого билда, для точной'
                                               f' информации стоить посмотреть гайд на форуме со всеми вариациями')
    elif call.data == 'back':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        get_classes(call.message)





# user_id[call.from_user.id]
bot.polling(none_stop=True, interval=0)






