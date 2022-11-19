from common_data import get_markup, HEALTH_ENTRY, HEALTH_COLLECT
from telegram import Update
from telegram.ext import (
    CallbackContext,
)

def add_health(update: Update, context: CallbackContext) -> int:
    context.user_data['type'] = 'health'
    reply_keyboard = ['Problem with right eye', 'Problem with left eye',
                      'Problem with both eyes', 'Vet visit']
    update.message.reply_text("Health issues:",
                              reply_markup=get_markup(reply_keyboard))
    return HEALTH_ENTRY

def add_health_comment(update: Update, context: CallbackContext):
    context.user_data["occasion"] = update.callback_query.data
    context.bot.send_message(text="Write your comment, please", chat_id=update.callback_query.message.chat_id)
    return HEALTH_COLLECT
