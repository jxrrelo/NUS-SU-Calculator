#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import inflect
import os

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove,
                      InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

PORT = int(os.environ.get('PORT', 5000))

users = []

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# States for conversation
CGPA, GRADED_CU, MODS_THIS_SEM, GRADES, LETTERS = range(5)

# Grade points according to letter grade
grades_dict = {"A+": 5.0, "A": 5.0, "A-": 4.5, "B+": 4.0, "B": 3.5,
               "B-": 3.0, "C+": 2.5, "C": 2.0, "D+": 1.5, "D": 1.0, "F": 0.0}


def start(update, context):
    user = update.message.from_user

    if not user.username in users:
        users.append(user.username)
        logger.info("User %s started the conversation.", user.username)
        logger.info("Users to date: %s", len(users))

    update.message.reply_text(
        "Hey " + user.first_name +
        "! Let's do some Math and see which mods should we S/U"
        "\n\nSo first, what's your overall CAP (This refers to your weighted average CAP across all your completed semesters, inclusive of the results released on 9th June)"
    )
    return CGPA


def collect_cgpa(update, context):
    cgpa = update.message.text

    if (float(cgpa) < 0.0 or float(cgpa) > 5.0):
        update.message.reply_text("Are you sure your in NUS? Your CAP must be within 0.0 and 5.0. Please try again.\n\n"
                                  "So, what's your cumulative CAP (Include the latest grades released)"
                                  )
        return CGPA
    else:
        context.user_data['CGPA'] = float(cgpa)
        update.message.reply_text("I see, your CAP thus far is " + cgpa +
                                  "\n\nHow many graded MCs have you done? (including this sem)"
                                  )
        return GRADED_CU


def collect_graded_CUs(update, context):
    gCUs = update.message.text
    user_data = context.user_data
    user = update.message.from_user
    context.user_data['gCUs'] = float(gCUs)

    if 0 < float(gCUs) < 16:
        update.message.reply_text(
            user.first_name + ", I see you haven't done much so far. Please try again with /start when you've done enough!")
        user_data.clear()
        return ConversationHandler.END
    elif float(gCUs) < 0:
        update.message.reply_text(
            "Hmm... Negative number of MCs? Please try again with /start.")
        user_data.clear()
        return ConversationHandler.END
    elif float(gCUs) > 300:
        update.message.reply_text(
            user.first_name + ", either you have made a typo error or you must be a genius! Please try again with /start.")
        user_data.clear()
        return ConversationHandler.END
    else:
        update.message.reply_text("Number of graded MCs you have taken including this semester = " + gCUs
                                  + "\n\nHow many graded modules are you taking this sem? Take care when overloading beyond the usual 5 mods"
                                  )
        return MODS_THIS_SEM


def collect_mods_this_sem(update, context):
    num_of_mod = update.message.text
    user_data = context.user_data
    user = update.message.from_user
    mc_keyboard = [['2'], ['3'], ['4']]

    if float(num_of_mod) <= 0:
        update.message.reply_text(
            user.first_name + ",  I see you have keyed in wrongly hmmm... Let me know agan!")
        user_data.clear()
        return ConversationHandler.END
    elif ((int(num_of_mod) * 0.5) > context.user_data['gCUs']) or int(num_of_mod) > 10:
        update.message.reply_text("Wow!!!! Are you sure you have done " + num_of_mod + " modules this semester?"
                                  "\n\n Try again! How many modules are you taking this sem? "
                                  )
        return MODS_THIS_SEM
    else:
        try:
            context.user_data['mods'] = int(num_of_mod)
            update.message.reply_text("Number of modules this semester = " + num_of_mod +
                                      "\nHow many MC(s) is the 1st module?", reply_markup=ReplyKeyboardMarkup(mc_keyboard, one_time_keyboard=True))
        except:
            context.user_data['mods'] = round(float(num_of_mod), 0)
            update.message.reply_text("Number of modules this semester = " + num_of_mod + ". Let me just round it up to " + str(context.user_data['mods']) + " for you!"
                                      "\n\nHow many MC(s) is the 1st module?", reply_markup=ReplyKeyboardMarkup(mc_keyboard, one_time_keyboard=True))

    context.user_data['grades'] = []
    context.user_data['temp_cus'] = 0

    return GRADES


def collect_grades(update, context):

    p = inflect.engine()
    cu = update.message.text
    user_data = context.user_data
    user = update.message.from_user

    if float(cu) > context.user_data['gCUs']:
        update.message.reply_text("Hmmm you sure? I don't think that's possible"
                                  "\nPlease enter the MCs again")
        return GRADES
    elif context.user_data['temp_cus'] + float(cu) > context.user_data['gCUs']:
        update.message.reply_text("Sorry " + user.first_name + ", there seem to be some issue with the calculations."
                                  "\n\nWe need to restart this again.")
        user_data.clear()
        return ConversationHandler.END
    else:
        context.user_data['temp_cus'] += float(cu)

    if len(context.user_data['grades']) < context.user_data['mods']:
        i = len(context.user_data['grades'])+1
        reply_keyboard = [['A+'], ['A'], ['A-'], ['B+'], ['B'],
                          ['B-'], ['C+'], ['C'], ['D+'], ['D'], ['F']]
        update.message.reply_text("Mind sharing your grade for the " + p.ordinal(
            i) + " module?", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        context.user_data['grades_temp'] = float(cu)
        return LETTERS


def collect_letter_grades(update, context):
    p = inflect.engine()
    letter_grade = update.message.text.upper()
    i = len(context.user_data['grades'])+1
    context.user_data['grades'].append(
        [letter_grade, context.user_data['grades_temp'], grades_dict[letter_grade]])

    i = len(context.user_data['grades'])+1

    if i <= context.user_data['mods']:
        mc_keyboard = [['2'], ['3'], ['4']]
        update.message.reply_text("How many MCs is the " +
                                  p.ordinal(i) + " module?", reply_markup=ReplyKeyboardMarkup(mc_keyboard, one_time_keyboard=True))
        return GRADES
    else:
        context.user_data['grades'] = sorted(sorted(
            context.user_data['grades'], key=lambda x: x[1]), key=lambda x: x[-1], reverse=True)
        user_data = context.user_data

        max_gpa = {'gpa': context.user_data['CGPA'], 'mods': []}
        num_of_gmod = user_data['gCUs']
        cgpa = user_data['CGPA']
        this_sem = user_data['grades']
        cgpa *= num_of_gmod  # current total grade point

        counter = 0
        output = ""
        for i in this_sem[::-1]:
            num_of_gmod -= i[1]  # current number of cu - mod cu

            cgpa -= (i[2] * i[1])  # current gp - module gpa

            try:
                current_gpa = round((cgpa/num_of_gmod), 2)
            except:
                current_gpa = 0.00

            if (current_gpa > max_gpa['gpa']):
                max_gpa['gpa'] = current_gpa
                max_gpa['mods'].append(i)

            if (max_gpa['gpa'] > 5):
                update.message.reply_text(
                    "The grades you have keyed in for this semester suggests that you have already "
                    "attained a CAP of > 5 before this semester!\n\nType '/start' to calculate again.")
                user_data.clear()
                return ConversationHandler.END

            else:
                if(counter == 0):
                    output += "S/U the " + i[0] + " module with " + str(
                        i[1]) + " MCs, CAP = " + str(current_gpa)
                else:
                    output += "\nS/U another " + i[0] + " module with " + str(
                        i[1]) + " MCs, CAP = " + str(current_gpa)

                counter += 1

        output += "\n\nWe calculated and the highest CAP possible is " + \
            str(max_gpa['gpa']) + \
            "\n\nHere's the next step recommended for you! "

        if len(max_gpa['mods']) == 0:
            output += "\nWell, good news! You don't need to S/U any modules."
        else:
            output += "\nThese modules should be S/U-ed:"
            for i in max_gpa['mods']:
                output += "\n-\t\t" + \
                    str(i[1]) + " MCs module with " + str(i[0])

        update.message.reply_text(
            output + "\n\nNote: This system calculates the max CAP achievable without accounting for any S/U limitations. You may refer back to the step-by-step S/U flow to make a better decision.\n\nType '/start' to calculate again")

        user_data.clear()
        return ConversationHandler.END


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s ended the conversation.", user.first_name)
    logger.info("Users to date: %s", len(users))
    update.message.reply_text("\n\nType '/start' to calculate again",
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def help_doc(update, context):
    update.message.reply_text("Let's find out which modules to S/U to get the highest cumulative CAP. To begin, type '/start'"
                              "\n\nUnresponsive bot? You could have pressed something wrongly or type '/stop' to restart the bot.",
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def credits(update, context):
    update.message.reply_text("Thank you for using this! Hope it did help you make a better decision! We will be upgrading this to include more features! Stay tuned :) " + "\n\nIf you have any cool ideas or feedback please do let us know!",
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(update, context):
    update.message.reply_text("Hmmm.. there seems to be something wrong. Please try again!",
                              reply_markup=ReplyKeyboardRemove())
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(
        "1066494588:AAGLeeKyF4ySXf61_kRq_IP0OvIhhx5Ak5w", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        # [0]\.[0]|[0-4]\.(\d?\d?)|[4].[3]|[0-4]$
        states={
            CGPA: [MessageHandler(Filters.regex(r"^[0-9]\.[0-9][0-9]|[0-9]\.[0-9]|[0-9]$"), collect_cgpa)
                   ],

            GRADED_CU: [MessageHandler(Filters.regex(r"^[1-9][0-9]\.[05]|[0-9]\.[05]|[1-9][0-9]|[0-9]$"), collect_graded_CUs)
                        ],

            MODS_THIS_SEM: [MessageHandler(Filters.regex(r"^[0]\.[0]|[1][0-2]|[0-9]$"), collect_mods_this_sem)
                            ],

            GRADES: [MessageHandler(Filters.regex(r"^[234]$"), collect_grades),
                     ],

            LETTERS: [MessageHandler(Filters.regex(r"^[A-C][+-]|[a-c][+-]|[D]\+|[d+]\+|[A-F]|[a-f]$"), collect_letter_grades)
                      ],
        },

        fallbacks=[CommandHandler('stop', cancel),
                   CommandHandler('help', help_doc),
                   (CommandHandler('credits', credits))]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path='1066494588:AAGLeeKyF4ySXf61_kRq_IP0OvIhhx5Ak5w')

    updater.bot.setWebhook('https://arcane-beach-85347.herokuapp.com/' +
                           '1066494588:AAGLeeKyF4ySXf61_kRq_IP0OvIhhx5Ak5w')


# Run the bot until you press Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT. This should be used most of the time, since
# start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
