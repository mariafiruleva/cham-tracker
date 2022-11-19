from common_data import get_markup, FOOD_ENTRY, FOOD_ITEMS, FOOD_COLLECT
from telegram import Update
from telegram.ext import (
    CallbackContext, )


def add_food(update: Update, context: CallbackContext) -> int:
    context.user_data['type'] = 'food'
    reply_keyboard = ['Сricket', 'Cockroach', 'Worm-worm']
    update.message.reply_text("Select food type, please:",
                              reply_markup=get_markup(reply_keyboard))
    return FOOD_ENTRY

def add_items(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    context.user_data["food_type"] = update.callback_query.data
    reply_keyboard = [1, 2, 3, 4, 5, 6]
    context.bot.send_message(text=f'The amount of consumed {context.user_data["food_type"]}:',
                             chat_id=query.message.chat_id,
                             reply_markup=get_markup(reply_keyboard, n_cols=2)
                             )
    return FOOD_ITEMS

def add_food_comment(update: Update, context: CallbackContext):
    print("ADD FOOD")
    print(update.callback_query)
    context.user_data["items"] = float(update.callback_query.data)
    context.bot.send_message(text="Write your comment, please", chat_id=update.callback_query.message.chat_id)
    return FOOD_COLLECT