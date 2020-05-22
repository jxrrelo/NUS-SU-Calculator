from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove,
                      InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, CallbackQueryHandler)


def main():
    updater = Updater(
        "1276812405:AAHonZgGP3zIRAoKXDyhQqKlNaRohW_exEU", use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', start))

    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    updater.start_polling()

    updater.idle()


def start(update, context):
    keyboard = [[InlineKeyboardButton("Option 1", callback_data='1'), InlineKeyboardButton(
        "Option 2", callback_data='2')], [InlineKeyboardButton("Option 3", callback_data='3')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def button(update, context):
    query = update.callback_query
    query.edit_message_text(text="Selected option: {}".format(query.data))


if __name__ == '__main__':
    main()
