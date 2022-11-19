import csv
import datetime
import io

import gspread
import pandas as pd
from behavior import add_behavior, add_behavior_comment
from common_data import (get_markup, TABLE_ENTRY,
                         MED_ENTRY, MED_DRUG_NAME, MED_COLLECT, WRITE_MEDS_INFO,
                         HEALTH_ENTRY, HEALTH_COLLECT, WRITE_HEALTH_INFO,
                         BEHAVIOR_ENTRY, BEHAVIOR_COLLECT, WRITE_BEHAVIOR_INFO,
                         WATER_ENTRY, WATER_COLLECT, WRITE_WATER_INFO,
                         SHEDDING_ENTRY, SHEDDING_COLLECT, WRITE_SHEDDING_INFO,
                         FOOD_ENTRY, FOOD_ITEMS, FOOD_COLLECT, WRITE_FOOD_INFO)
from config import BOT_TOKEN, CREDS_JSON
from food import add_food, add_items, add_food_comment
from get_table import get_table
from health import add_health, add_health_comment
from meds import add_drug, add_drug_name, add_drug_comment
from oauth2client.service_account import ServiceAccountCredentials
from shedding import add_shedding, add_shedding_comment
from telegram import ReplyKeyboardRemove, Update
from telegram.ext import MessageHandler, Filters
from telegram.ext import (
    Updater,
    CommandHandler,
    ConversationHandler,
    CallbackContext,
    CallbackQueryHandler
)
from water import add_water, add_water_comment


# Variables
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive.file',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_JSON, scope)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('hi! I can help to track daily activity of your chameleon :) press /help, if you are interested')

def help(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("commands with 'add' prefix allow me to write input info in the google-table. "
                              "using /get_table table command, you can retrieve required information \n\n"
                              "/add_food -- add info about eating behavior to the table \n\n"
                              "/add_water -- add info about drinking behavior to the table \n\n "
                              "/add_behavior -- add info about behavior to the table \n\n"
                              "/add_health -- add info about health (problems, vet visit) to the table \n\n"
                              "/add_drug -- add info about drugs to the table \n\n"
                              "/add_shedding -- add info about shedding to the table \n\n"
                              "/get_table -- download the table")

def collect_info(update: Update, context: CallbackContext) -> int:
    context.user_data['date'] = datetime.date.today().strftime("%d/%m/%Y")
    context.user_data["comment"] = update.message.text
    if context.user_data['type'] == 'food':
        if context.user_data['items'] > 1:
            food_type = f'{context.user_data["food_type"]}s'
        else:
            food_type = context.user_data["food_type"]
        text = f'Information which you want to add:\n\n' \
               f'Date: {context.user_data["date"]};\n' \
               f'Food type: {food_type};\n' \
               f'Amount: {context.user_data["items"]}.\n\n' \
               f'Your comment:\n\n{context.user_data["comment"]}'
    if context.user_data['type'] == 'shedding':
        text = f'Information which you want to add:\n\n' \
               f'Date: {context.user_data["date"]};\n' \
               f'Shedding part: {context.user_data["shedding_part"]}.\n\n' \
               f'Your comment:\n\n{context.user_data["comment"]}'
    if context.user_data['type'] == 'health':
        text = f'Information which you want to add:\n\n' \
               f'Date: {context.user_data["date"]};\n' \
               f'Health occasion = {context.user_data["occasion"]}.\n\n' \
               f'Your comment:\n\n{context.user_data["comment"]}'
    if context.user_data['type'] == 'water':
        text = f'Information which you want to add:\n\n' \
               f'Date: {context.user_data["date"]};\n' \
               f'Water behavior: {context.user_data["water_behavior"]}.\n\n' \
               f'Your comment:\n\n{context.user_data["comment"]}'
    if context.user_data['type'] == 'behavior':
        text = f'Information which you want to add:\n\n' \
               f'Date: {context.user_data["date"]};\n' \
               f'Behavior: {context.user_data["behavior"]}.\n\n' \
               f'Your comment:\n\n{context.user_data["comment"]}'
    if context.user_data['type'] == 'meds':
        text = f'Information which you want to add:\n\n' \
               f'Date: {context.user_data["date"]};\n' \
               f'Drug type: {context.user_data["drug_type"]}; \n' \
               f'Drug name = {context.user_data["name"]}.\n\n' \
               f'Your comment:\n\n{context.user_data["comment"]}'
    reply_keyboard = ['OK', 'Cancel']
    context.bot.send_message(text=text, chat_id=update.message.chat_id,
        reply_markup=get_markup(reply_keyboard)
    )
    if context.user_data['type'] == 'meds':
        return WRITE_MEDS_INFO
    if context.user_data['type'] == 'food':
        return WRITE_FOOD_INFO
    return WRITE_INFO

def write_info(update: Update, context: CallbackContext):
    if update.callback_query.data == 'OK':
        client = gspread.authorize(creds)
        if context.user_data['type'] == 'food':
            sheet = client.open('cham_info').worksheet('food')
            data = sheet.get_all_records()
            row_to_insert = [context.user_data['date'], context.user_data['food_type'],
                             context.user_data['items'], context.user_data['comment']]
        if context.user_data['type'] == 'shedding':
            sheet = client.open('cham_info').worksheet('shedding')
            data = sheet.get_all_records()
            row_to_insert = [context.user_data['date'], context.user_data['shedding_part'], context.user_data['comment']]
        if context.user_data['type'] == 'health':
            sheet = client.open('cham_info').worksheet('health')
            data = sheet.get_all_records()
            row_to_insert = [context.user_data['date'], context.user_data['occasion'], context.user_data['comment']]
        if context.user_data['type'] == 'water':
            sheet = client.open('cham_info').worksheet('water')
            data = sheet.get_all_records()
            row_to_insert = [context.user_data['date'], context.user_data['water_behavior'], context.user_data['comment']]
        if context.user_data['type'] == 'behavior':
            sheet = client.open('cham_info').worksheet('behavior')
            data = sheet.get_all_records()
            row_to_insert = [context.user_data['date'], context.user_data['behavior'], context.user_data['comment']]
        if context.user_data['type'] == 'meds':
            sheet = client.open('cham_info').worksheet('meds')
            data = sheet.get_all_records()
            row_to_insert = [context.user_data['date'], context.user_data['drug_type'], context.user_data["name"],
                             context.user_data["comment"]]
        sheet.insert_row(row_to_insert,
                         len(data) + 2)
        update.effective_message.reply_text("Updates were saved")
    else:
        update.effective_message.reply_text("Updates were not saved", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def sent_table(update: Update, context: CallbackContext):
    query = update.callback_query
    client = gspread.authorize(creds)
    answer = update.callback_query.data
    sheet = client.open('cham_info').worksheet(answer.lower())
    data = sheet.get_all_records()
    date = datetime.date.today().strftime("%d_%m_%Y")
    s = io.StringIO()
    print(data)
    csv.writer(s).writerows(pd.DataFrame(data).T.reset_index().values.T.tolist())
    s.seek(0)
    buf = io.BytesIO()
    buf.write(s.getvalue().encode())
    buf.seek(0)
    buf.name = f'chameleon_{answer.lower()}_sheet_{date}.csv'
    context.bot.send_document(query.message.chat_id, document=buf)
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("I'll not write your answers to the table. Bye :)", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def main() -> None:
    updater = Updater(BOT_TOKEN, use_context=True)
    food_handler = ConversationHandler(
        entry_points=[CommandHandler('add_food', add_food)],
        states={
            FOOD_ENTRY: [CallbackQueryHandler(add_items)],
            FOOD_ITEMS: [CallbackQueryHandler(add_food_comment)],
            FOOD_COLLECT: [MessageHandler(Filters.text, collect_info)],
            WRITE_FOOD_INFO: [CallbackQueryHandler(write_info)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    drugs_handler = ConversationHandler(
        entry_points=[CommandHandler('add_drug', add_drug)],
        states={
            MED_ENTRY: [CallbackQueryHandler(add_drug_name)],
            MED_DRUG_NAME: [MessageHandler(Filters.text, add_drug_comment)],
            MED_COLLECT: [MessageHandler(Filters.text, collect_info)],
            WRITE_MEDS_INFO: [CallbackQueryHandler(write_info)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    shedding_handler = ConversationHandler(
        entry_points=[CommandHandler('add_shedding', add_shedding)],
        states={
            SHEDDING_ENTRY: [CallbackQueryHandler(add_shedding_comment)],
            SHEDDING_COLLECT: [MessageHandler(Filters.text, collect_info)],
            WRITE_SHEDDING_INFO: [CallbackQueryHandler(write_info)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    health_handler = ConversationHandler(
        entry_points=[CommandHandler('add_health', add_health)],
        states={
            HEALTH_ENTRY: [CallbackQueryHandler(add_health_comment)],
            HEALTH_COLLECT: [MessageHandler(Filters.text, collect_info)],
            WRITE_HEALTH_INFO: [CallbackQueryHandler(write_info)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    water_handler = ConversationHandler(
        entry_points=[CommandHandler('add_water', add_water)],
        states={
            WATER_ENTRY: [CallbackQueryHandler(add_water_comment)],
            WATER_COLLECT: [MessageHandler(Filters.text, collect_info)],
            WRITE_WATER_INFO: [CallbackQueryHandler(write_info)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    behavior_handler = ConversationHandler(
        entry_points=[CommandHandler('add_behavior', add_behavior)],
        states={
            BEHAVIOR_ENTRY: [CallbackQueryHandler(add_behavior_comment)],
            BEHAVIOR_COLLECT: [MessageHandler(Filters.text, collect_info)],
            WRITE_BEHAVIOR_INFO: [CallbackQueryHandler(write_info)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    table_handler = ConversationHandler(
        entry_points=[CommandHandler('get_table', get_table)],
        states={
            TABLE_ENTRY: [CallbackQueryHandler(sent_table)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("help", help))
    updater.dispatcher.add_handler(health_handler)
    updater.dispatcher.add_handler(food_handler)
    updater.dispatcher.add_handler(water_handler)
    updater.dispatcher.add_handler(shedding_handler)
    updater.dispatcher.add_handler(behavior_handler)
    updater.dispatcher.add_handler(table_handler)
    updater.dispatcher.add_handler(drugs_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
