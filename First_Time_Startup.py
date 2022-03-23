
def _rollbot_config():
    name = input("Enter bot token")
    f = open("config.ini", "w")

    f.write("[BOT]\nRollBot = %s\n[ADMIN]\nadminID = 393122454236692480" % name)
    f.close()

_rollbot_config()