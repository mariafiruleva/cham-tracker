from common_data import get_markup, BEHAVIOR_ENTRY, BEHAVIOR_COLLECT
from telegram import Update
from telegram.ext import (
    CallbackContext,
)

def add_behavior(update: Update, context: CallbackContext) -> int:
    context.user_data['type'] = 'behavior'
    reply_keyboard = ["Didn't leave the terrarium", "Actively asked to come out",
                       "Crawled across the sofa", "Didn't walk around the room", "Walked actively",
                      "Closed eyes"]
    update.message.reply_text("Was Zephyrka a good boy today? :)",
                              reply_markup=get_markup(reply_keyboard))
    return BEHAVIOR_ENTRY

def add_behavior_comment(update: Update, context: CallbackContext):
    context.user_data["behavior"] = update.callback_query.data
    context.bot.send_message(text="Write your comment, please", chat_id=update.callback_query.message.chat_id)
    return BEHAVIOR_COLLECT