from app import bot
from . import mailcheck
import threading

threading.Thread(target = mailcheck.run).start()

print("Mail plugin loaded.")
