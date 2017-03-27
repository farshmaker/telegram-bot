import sys
import time
import telepot
import requests
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

def get_headers():
    api_token = '5661234332'
    header = {'Content-Type': 'application/json', 'Token': api_token}
    return header

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    if msg['text'] == '/events':
        r = requests.get(url = 'http://api.events.nesterione.com/api/v0.1/events', 
            headers = get_headers())
        for event in r.json():
            print(event['title'])
            keyboard = [InlineKeyboardButton("Option 1", callback_data='1')]

            reply_markup = InlineKeyboardMarkup(keyboard)
            
            bot.sendMessage(chat_id, 'Запланированные ивенты:', reply_markup = reply_markup)
def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)

    bot.answerCallbackQuery(query_id, text='Got it')

TOKEN = sys.argv[1]  # get token from command-line

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print ('Listening ...')


# Keep the program running.
while 1:
    time.sleep(10)

# import logging
# from telegram import InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     level=logging.INFO)


# def start(bot, update):
#     keyboard = [[InlineKeyboardButton("Option 1", callback_data='1'),
#                  InlineKeyboardButton("Option 2", callback_data='2')],

#                 [InlineKeyboardButton("Option 3", callback_data='3')]]

#     reply_markup = InlineKeyboardMarkup(keyboard)

#     update.message.reply_text('Please choose:', reply_markup=reply_markup)


# def button(bot, update):
#     query = update.callback_query

#     bot.editMessageText(text="Selected option: %s" % query.data,
#                         chat_id=query.message.chat_id,
#                         message_id=query.message.message_id)


# def help(bot, update):
#     update.message.reply_text("Use /start to test this bot.")


# def error(bot, update, error):
#     logging.warning('Update "%s" caused error "%s"' % (update, error))


# # Create the Updater and pass it your bot's token.
# updater = Updater("TOKEN")

# updater.dispatcher.add_handler(CommandHandler('start', start))
# updater.dispatcher.add_handler(CallbackQueryHandler(button))
# updater.dispatcher.add_handler(CommandHandler('help', help))
# updater.dispatcher.add_error_handler(error)

# # Start the Bot
# updater.start_polling()

# # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
# # SIGTERM or SIGABRT
# updater.idle()