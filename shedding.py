from common_data import get_markup, SHEDDING_ENTRY, SHEDDING_COLLECT
from telegram import Update
from telegram.ext import (
    CallbackContext,
)


def add_shedding(update: Update, context: CallbackContext) -> int:
    context.user_data['type'] = 'shedding'
    reply_keyboard = ['Head', 'Body', 'Legs']
    update.message.reply_text("Select shedding part, please:",
                              reply_markup=get_markup(reply_keyboard))
    return SHEDDING_ENTRY

def add_shedding_comment(update: Update, context: CallbackContext):
    context.user_data["shedding_part"] = update.callback_query.data
    context.bot.send_message(text="Write your comment, please", chat_id=update.callback_query.message.chat_id)
    return SHEDDING_COLLECT