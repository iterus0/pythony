import config
import telebot

bot = telebot.TeleBot(config.token)

import app.plugins.mail
import app.plugins.schedule
