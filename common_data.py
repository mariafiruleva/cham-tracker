from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
  menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
  if header_buttons:
    menu.insert(0, header_buttons)
  if footer_buttons:
    menu.append(footer_buttons)
  return menu

def get_markup(reply_keyboard, n_cols=1):
    button_list = [InlineKeyboardButton(x, callback_data=x) for x in reply_keyboard]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=n_cols))
    return(reply_markup)

MED_ENTRY, MED_DRUG_NAME, MED_COLLECT, WRITE_MEDS_INFO = range(4)
HEALTH_ENTRY, HEALTH_COLLECT, WRITE_HEALTH_INFO = range(3)
BEHAVIOR_ENTRY, BEHAVIOR_COLLECT, WRITE_BEHAVIOR_INFO = range(3)
WATER_ENTRY, WATER_COLLECT, WRITE_WATER_INFO = range(3)
SHEDDING_ENTRY, SHEDDING_COLLECT, WRITE_SHEDDING_INFO = range(3)
FOOD_ENTRY, FOOD_ITEMS, FOOD_COLLECT, WRITE_FOOD_INFO = range(4)
TABLE_ENTRY = range(1)