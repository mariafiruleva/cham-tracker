from common_data import get_markup
from telegram import Update
from telegram.ext import (
    CallbackContext,
)

MED_ENTRY, MED_DRUG_NAME, MED_COLLECT, WRITE_MEDS_INFO = range(4)


def add_drug(update: Update, context: CallbackContext) -> int:
    context.user_data['type'] = 'meds'
    reply_keyboard = ['Tablets', 'Drops']
    update.message.reply_text("Type of the med:",
                              reply_markup=get_markup(reply_keyboard))
    return MED_ENTRY

def add_drug_name(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    context.user_data["drug_type"] = update.callback_query.data
    context.bot.send_message(text="Write the drug name to me, please", chat_id=query.message.chat_id)
    return MED_DRUG_NAME

def add_drug_comment(update: Update, context: CallbackContext):
    context.user_data["name"] = update.message.text
    context.bot.send_message(text="Write your comment, please", chat_id=update.message.chat_id)
    return MED_COLLECT
