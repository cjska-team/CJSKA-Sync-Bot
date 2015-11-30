import sys
from bot import Bot

try:
    username = str(sys.argv[1])
    password = str(sys.argv[2])
    bot = Bot(username, password, (1 * 60))
    bot.run()
except IndexError:
    print("Please provide a username and password!")