import logging
import requests
import json
import constants
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

def get_headers():
    api_token = constants.API_TOKEN
    header = {'Content-Type': 'application/json', 'Token': api_token}
    return header

def event_list(bot, update):
    r = requests.get(url = 'http://api.events.nesterione.com/api/v0.1/events', headers = get_headers())

    keyboard = []
    for event in r.json():
        keyboard.append([InlineKeyboardButton(event['title'], callback_data = event['_id'])])

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Events:', reply_markup=reply_markup)

def button(bot, update):
    query = update.callback_query
    words = query.data.split(constants.DATA_SEPARATOR)
    event_id = words[0]
    user_name = query['from_user']['first_name']
    attendees = get_attendees(event_id)

    logging.info(user_name)

    if len(attendees) > 0:
        for attendee in attendees:
            if attendee['name'] == user_name:
                attendee_id = attendee['id']
                command = constants.DELETE_COMMAND
        if "attendee_id" not in locals():
            command = constants.ADD_COMMAND
    else:
        command = constants.ADD_COMMAND
    if len(words) == 2:
        data = {'name':user_name, 'notes':''}

        if command == constants.ADD_COMMAND:
            url = 'http://api.events.nesterione.com/api/v0.1/events/' + event_id + '/attendees'
            r = requests.put(url, data = json.dumps(data), headers = get_headers())
            command = constants.DELETE_COMMAND

        elif command == constants.DELETE_COMMAND:
            url = 'http://api.events.nesterione.com/api/v0.1/events/' + event_id + '/attendees/' + str(attendee_id)
            requests.delete(url, headers = get_headers())
            command = constants.ADD_COMMAND

        attendees = get_attendees(event_id)

    callback_data = event_id + command
    keyboard = [[InlineKeyboardButton(constants.KEYBOARD_TITLE[command], callback_data = callback_data)]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    if len(attendees) > 0:
        text = '\n'.join('{}: {}'.format(i + 1, v['name']) for i, v in enumerate(attendees))
    else:
        text = "There is no attendees:("

    bot.editMessageText(text = text,
                        chat_id = query.message.chat_id,
                        message_id = query.message.message_id,
                        reply_markup = reply_markup)
    if len(words) == 2:
        bot.answerCallbackQuery(query.id, text=constants.CALLBACK_ANSWER[command])

def help(bot, update):
    update.message.reply_text("Use /events to get list of events.")


def error(bot, update, error):
    logging.warning('Update "%s" caused error "%s"' % (update, error))

def get_attendees(event_id):
    r = requests.get(url = 'http://api.events.nesterione.com/api/v0.1/events/' + event_id, headers = get_headers())
    event_info = r.json()
    return event_info['attendees']

updater = Updater(constants.TOKEN)

updater.dispatcher.add_handler(CommandHandler('events', event_list))
updater.dispatcher.add_handler(CallbackQueryHandler(button))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_error_handler(error)

updater.start_polling()

updater.idle()