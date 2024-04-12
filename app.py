import telebot

from config import TOKEN, keys
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = ('Это чат бот для конвертации валюты \nчтобы начать работу введите команду боту в следующем формате:'
'\n<имя валюты>  <в какую валюту перевести> <количество переводимой валюты>\nУвидеть список доступных валют: /values'
'\nпомощь: /help')
    bot.reply_to(message, text)


@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'чтобы начать работу введите команду боту в следующем формате: \n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\nУвидеть список доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n' .join((text, key, ))  
    bot.reply_to(message, text)    

@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message): 
    try:
        values = message.text.split(' ')   

        if len(values) > 3:
            raise APIException('Cлишком много параметров.')
        elif len(values) < 3:
            raise APIException('Мало параметров.')
        quote, base, amount = values
        total_base = CurrencyConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:        
        result = total_base * float(amount)
        text = f'Цена {amount} {quote} в {base} - {result}'
        bot.send_message(message.chat.id, text)   

bot.polling()