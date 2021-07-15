from webBot import WebBot

bot = WebBot("C:\Program Files (x86)\chromedriver.exe")

bot.login("${username}", "${password}")
bot.getFollowers()
bot.comment()
