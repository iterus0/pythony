from app import bot
import time


def main():
    try:
        bot.polling(none_stop=True)

    except Exception as e:
        print(e)
        time.sleep(5)


if __name__ == '__main__':
    main()
