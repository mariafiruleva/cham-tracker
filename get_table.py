from common_data import get_markup, TABLE_ENTRY
from telegram import Update
from telegram.ext import (
    CallbackContext,
)


def get_table(update: Update, context: CallbackContext) -> int:
    reply_keyboard = ['Food', 'Water', 'Health', 'Shedding', 'Behavior']
    update.message.reply_text("Which sheet do you want to download?",
                              reply_markup=get_markup(reply_keyboard))
    return TABLE_ENTRY

