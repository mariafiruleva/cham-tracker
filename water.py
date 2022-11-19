from common_data import get_markup, WATER_ENTRY, WATER_COLLECT
from telegram import Update
from telegram.ext import (
    CallbackContext,
)


def add_water(update: Update, context: CallbackContext) -> int:
    context.user_data['type'] = 'water'
    reply_keyboard = ['Drank water (normally)', 'Drank water (more than usual)',
                       "Drank water (less than usual)", "Didn't drink water"]
    update.message.reply_text('What about water?', reply_markup=get_markup(reply_keyboard))
    return WATER_ENTRY

def add_water_comment(update: Update, context: CallbackContext):
    context.user_data["water_behavior"] = update.callback_query.data
    context.bot.send_message(text="Write your comment, please", chat_id=update.callback_query.message.chat_id)
    return WATER_COLLECT