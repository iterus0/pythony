import config
import time
from app import bot
from . import mail_utils


def run():
    while True:
        new_msgs = mail_utils.get_new_messages()

        if len(new_msgs) > 0:
            notify_chat(new_msgs)

        time.sleep(10)


def notify_chat(new_msgs):
    reply = "На почте *{}* новых сообщений\n".format( len(new_msgs) )

    for msg in new_msgs:
        (sender, subject) = msg

        reply += "*От:* {0}\n*Тема:* {1}\n".format(sender, subject)

    bot.send_message(config.chat_id, reply, parse_mode="Markdown")
