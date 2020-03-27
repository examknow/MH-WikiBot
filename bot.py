import QuIRC
import random
import requests
import re
import time
import random
topic = '' #channel topic for use in channels where quotebot runs
nick = 'WikiBotTester'
bot = QuIRC.IRCConnection()
lastgreeter = ''
greetings = [
    "Hello {}!",
    "Hi {}!",
    "Hello there {}!",
    "Hi there {}!",
    "Hey {}!"
]
owapikey = '' #place an api key for open weather map here
admins = ['Examknow', 'freenode-staff']
##FUNCTION FLAGS - SET TO 1 TO ENABLE
greetingsbot = 0
weatherbot = 0
linkbot = 0
quotebot = 0
pingbot = 0
buttbot = 0
cashortbot = 0
nspassword = ''

def getinfo():
    print('loadingconfig')
    global topic
    global nick
    global greetings
    global greetingsbot
    global weatherbot
    global quotebot
    global linkbot
    global pingbot
    global buttbot
    global cashortbot
    global admins
    global owapikey
    global nspassword
    infofile = open('settings.csv', 'r')
    for line in infofile:
        setting = line.split(';')
        print(setting)
        if setting[0] == 'topic':
            topic = setting[1]
        if setting[0] == 'nick':
            nick = setting[1]
        if setting[0] == 'greetings':
            greetings = setting[1].split(',')
        if setting[0] == 'greetingsbot':
            greetingsbot = int(setting[1])
        if setting[0] == 'weatherbot':
            weatherbot = int(setting[1])
        if setting[0] == 'owapikey':
            owapikey = setting[1]
        if setting[0] == 'quotebot':
            quotebot = int(setting[1])
        if setting[0] == 'linkbot':
            linkbot = setting[1]
        if setting[0] == 'pingbot':
            pingbot = int(setting[1])
        if setting[0] == 'buttbot':
            buttbot = setting[1]
        if setting[0] == 'cashortbot':
            cashortbot = int(setting[1])
        if setting[0] == 'admins':
            admins = setting[1]
            admins = admins.split(',')
        if setting[0] == 'nspassword':
            nspassword = setting[1]
def on_connect(bot):
    bot.set_nick(nick)
    bot.send_user_packet(nick)

def on_welcome(bot):
    global nspassword
    bot.send_message('NickServ', 'identify ' + nspassword)
    print('Authed to NickServ')
    time.sleep(10)
    bot.join_channel('#SigmaBot')
    print('Joined channels')
def on_message(bot, channel, sender, message):
    global topic
    global nick
    global lastgreeter
    global greetings
    global greetingsbot
    global weatherbot
    global quotebot
    global linkbot
    global pingbot
    global buttbot
    global cashortbot
    global admins
    global owapikey
    if message.lower().startswith('!userinfo'):
        arg = message.split(' ')
        wiki = arg[1]
        user = arg[2]
        S = requests.Session()
        URL = "https://" + wiki + ".miraheze.org/w/api.php"
        PARAMS = {
           "action": "query",
           "format": "json",
           "list": "users",
           "ususers": user,
           "usprop": "blockinfo|groups|editcount|registration|emailable|gender"
        }
        try:
                R = S.get(url=URL, params=PARAMS)
                DATA = R.json()
                USERS = DATA["query"]["users"]
                for u in USERS:
                        try:
                                if str(u["blockid"]) != '':
                                        bot.send_message(channel, str(u["name"]) + " (Blocked) has made " + str(u["editcount"]) + " edits on " + wiki + "wiki")
                        except KeyError:
                                bot.send_message(channel, str(u["name"]) + " has made " + str(u["editcount"]) + " edits on " + wiki + "wiki.")
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            bot.send_message(channel, "An error occured. Did you type the wiki incorrectly? Does the user exist?")
    if message.lower().startswith('!globaluser'):
       arg = message.split(' ')
       user = arg[1]
       S = requests.Session()
       URL = "https://meta.miraheze.org/w/api.php"
       PARAMS = {
          "action": "query",
          "format": "json",
          "list": "globaluserinfo",
          "guiuser": user,
          "guiprop": "editcount"
       }
       try:
               R = S.get(url=URL, params=PARAMS)
               DATA = R.json()
               GLOBALALLUSERS = DATA["query"]["globalallusers"]
               for u in GLOBALALLUSERS:
                   try:
                       if str(u["locked"]) == '':
                        bot.send_message(channel, str(u["name"]) + " (Globally Locked) has made " + str(u["editcount"]) + " edits on all Miraheze wikis")
                       except KeyError:
                           bot.send_message(channel, str(u["name"]) + " has made " + str(u["editcount"]) + " on all Miraheze wikis")
                   except ValueError:
                       bot.send_message(channel, "An error occured. Did you type the wiki incorrectly? Does the user exist?")
        
def on_pm(bot, sender, message):
    global topic
    global nick
    global lastgreeter
    global greetings
    global greetingsbot
    global weatherbot
    global quotebot
    global linkbot
    global pingbot
    global buttbot
    global cashortbot
    global admins
    global owapikey
    print('Got PM')
    if message.lower() == 'getinfo' and sender in admins:
        bot.set_nick(nick + '-down')
        bot.send_message(sender, 'Rebuilding')
        topic = ''
        nick = ''
        lastgreeter = ''
        greetings = ''
        owapikey = ''
        admins = ''
        greetingsbot = 0
        weatherbot = 0
        linkbot = 0
        quotebot = 0
        pingbot = 0
        buttbot = 0
        cashortbot = 0
        nspassword = ''
        time.sleep(1)
        getinfo()
        time.sleep(1)
        bot.send_message(sender, 'Rebuilt')
        bot.set_nick(nick)
getinfo()
bot.on_private_message.append(on_pm)
bot.on_connect.append(on_connect)
bot.on_welcome.append(on_welcome)
bot.on_public_message.append(on_message)
print('Starting...')

bot.connect("chat.freenode.net")
print('Connected')
bot.run_loop()
