import logging
import requests
import json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

def get_headers():
    api_token = '5661234332'
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
    words = query.data.split(":")
    event_id = words[0]
    keyboard = []
    user_name = query['from_user']['first_name']
    attendees = get_attendees(event_id)
    attendee_id = -1

    if attendees.size:
        for attendee in attendees:
            if attendee['name'] == user_name:
                attendee_id = attendee['id']


    keyboard = [[InlineKeyboardButton("Add me!", callback_data = event_id + ':add')]]

    if len(words) == 2:
        command = words[-1]
        data = {'name':user_name, 'notes':''}
        attendee_id = get_attendee_id(attendees, user_name)

        if command == 'add':
            url = 'http://api.events.nesterione.com/api/v0.1/events/' + event_id + '/attendees'
            r = requests.put(url, data = json.dumps(data), headers = get_headers())
            keyboard = [[InlineKeyboardButton("Remove me!", callback_data = event_id + ':del')]]

        elif command == 'del':
            url = 'http://api.events.nesterione.com/api/v0.1/events/' + event_id + '/attendees/' + str(attendee_id)
            requests.delete(url, headers = get_headers())

        attendees = get_attendees(event_id)

    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.editMessageText(text = '\n'.join('{}: {}'.format(i + 1, v['name']) for i, v in enumerate(attendees)),
                        chat_id = query.message.chat_id,
                        message_id = query.message.message_id,
                        reply_markup = reply_markup)

def help(bot, update):
    update.message.reply_text("Use /events to get list of events.")


def error(bot, update, error):
    logging.warning('Update "%s" caused error "%s"' % (update, error))

def get_attendees(event_id):
    r = requests.get(url = 'http://api.events.nesterione.com/api/v0.1/events/' + event_id, headers = get_headers())
    event_info = r.json()
    return event_info['attendees']

def get_attendee_id(attendees, user_name):
    for attendee in attendees:
        if 'name' in attendee and attendee['name'] == user_name:
            return attendee['id']

updater = Updater("329092132:AAEJl4dlsv3rgZ8Q5OkrBLB0mTdCM7oyOzQ")

updater.dispatcher.add_handler(CommandHandler('events', event_list))
updater.dispatcher.add_handler(CallbackQueryHandler(button))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_error_handler(error)

updater.start_polling()

updater.idle()