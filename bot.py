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
stewards = ['miraheze/Examknow', 'miraheze/RhinosF1', 'miraheze/John', 'wikipedia/The-Voidwalker', 'miraheze/Reception123']
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
    global flagpass
    global nonflagpass
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
        if setting[0] == 'flagpass':
            flagpass = setting[1]
	if setting[0] == 'nonflagpass':
            nonflagpass = setting[1]
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
    global flagpass
    global nonflagpass
    sendernick = sender.split("!")[0]
    senderhost = sender.split("@")[1]
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
           "usprop": "blockinfo|groupmemberships|editcount|registration|emailable|gender"
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
          "meta": "globaluserinfo",
          "guiuser": user,
          "guiprop": "editcount"
        }
        try:
                R = S.get(url=URL, params=PARAMS)
                DATA = R.json()
                GLOBALUSERINFO = DATA["query"]["globaluserinfo"]
                for u in GLOBALUSERINFO:
                        try:
                                if u["locked"] == '':
                                        bot.send_message(channel, u["name"] + " (Globally Locked) has made " + u["editcount"] + " edits on all Miraheze wikis")
                        except KeyError:
                                bot.send_message(channel, u["name"] + " has made " + u["editcount"] + " on all Miraheze wikis")
        except TypeError:
            print("TypeError when using !globaluser on " + channel)
            bot.send_message(channel, "An unexpected error has occured. I have reported this to Examknow.")
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            bot.send_message(channel, "An error occured. Did you type the wiki incorrectly? Does the user exist?") 
    
    if message.lower().startswith('!ca'):
        try:
            arg = message.split(' ')
            target = arg[1]
        except:
            bot.send_message(channel, "Syntax is !ca <user>")
            return
        bot.send_message(channel, "https://meta.miraheze.org/wiki/Special:CentralAuth/" + target)
    
    if message.lower().startswith('!blockuser') and senderhost in stewards:
        arg = message.split(' ')
        if len(arg) == 3:
            wiki = arg[1]
            user = arg[2]
            reason = arg[3]
        elif len(arg) > 3:
            wiki = arg[1]
            user = arg[2]
            reason = message.split(user, 1)[1]
        else:
            bot.send_message(channel, "Syntax is !blockuser <wiki> <user> <reason>")
            return

        S = requests.Session()

        URL = "https://" + wiki + ".miraheze.org/w/api.php"
        PARAMS_0 = {
            "action": "query",
            "meta": "tokens",
            "type": "login",
            "format": "json"
        }

        try:
            R = S.get(url=URL, params=PARAMS_0)
            DATA = R.json()
        except:
            bot.send_message(channel, "Catostrophic Error! Unable to connect to the wiki.")
            return

        LOGIN_TOKEN = DATA['query']['tokens']['logintoken']
        
        PARAMS_1 = {
        "action": "login",
        "lgname": "EkWikiBot",
        "lgpassword": nonflagpass,
        "lgtoken": LOGIN_TOKEN,
        "format": "json"
        }

        try:
            R = S.post(URL, data=PARAMS_1)
        except:
            bot.send_message(channel, "Catostrophic Error! Unable to login to the wiki.")

        PARAMS_2 = {
            "action": "query",
            "meta": "tokens",
            "format": "json"
        }

        try:
            R = S.get(url=URL, params=PARAMS_2)
            DATA = R.json()
        except:
            bot.send_message(channel, "Catostrophic Error! Unable to connect to the wiki.")
            return

        CSRF_TOKEN = DATA['query']['tokens']['csrftoken']

# Step 4: POST request to block user
        PARAMS_3 = {
            "action": "block",
            "user": user,
            "expiry": "infinite",
            "reason": "{{BotBlocked|user=" + sendernick + "|reason=" + reason + "}}",
            "bot": "false",
            "token": CSRF_TOKEN,
            "format": "json"
        }
    
        try:
            R = S.post(URL, data=PARAMS_3)
            DATA = R.json()

            bot.send_message(channel, "Block request sent. You may want to check https://" + wiki + ".miraheze.org/wiki/Special:Log?type=block&page=" + user + " to confirm that the block worked.")
        except:
            bot.send_message(channel, "An unexpected error occured. Did you type the wiki or user incorrectly? Do I have admin rights on that wiki?")
            return
        
    if message.lower().startswith('!unblockuser') and senderhost in stewards:
        arg = message.split(' ')
        if len(arg) == 3:
            wiki = arg[1]
            user = arg[2]
            reason = arg[3]
        elif len(arg) > 3:
            wiki = arg[1]
            user = arg[2]
            reason = message.split(user, 1)[1]
        else:
            bot.send_message(channel, "Syntax is !blockuser <wiki> <user> <reason>")
            return
        
        S = requests.Session()

        URL = "https://" + wiki + ".miraheze.org/w/api.php"

# Step 1: GET request to fetch login token
        PARAMS_0 = {
            "action": "query",
            "meta": "tokens",
            "type": "login",
            "format": "json"
        }

        try:
            R = S.get(url=URL, params=PARAMS_0)
            DATA = R.json()
        except:
            bot.send_message(channel, "Catostrophic Error! Unable to connect to the wiki.")
            return

        LOGIN_TOKEN = DATA['query']['tokens']['logintoken']

# Step 2: POST request to log in. Use of main account for login is not
# supported. Obtain credentials via Special:BotPasswords
# (https://www.mediawiki.org/wiki/Special:BotPasswords) for lgname & lgpassword
        PARAMS_1 = {
        "action": "login",
        "lgname": "EkWikiBot",
        "lgpassword": nonflagpass,
        "lgtoken": LOGIN_TOKEN,
        "format": "json"
        }
        try:
            R = S.post(URL, data=PARAMS_1)
        except:
            bot.send_message(channel, "Catostrophic Error! Unable to connect to the wiki.")
            return

# Step 3: GET request to fetch CSRF token
        PARAMS_2 = {
            "action": "query",
            "meta": "tokens",
            "format": "json"
        }

        try:
            R = S.get(url=URL, params=PARAMS_2)
            DATA = R.json()
        except:
            bot.send_message(channel, "Catostrophic Error! Unable to connect to the wiki.")
            return

        CSRF_TOKEN = DATA['query']['tokens']['csrftoken']

# Step 4: POST request to block user
        PARAMS_3 = {
            "action": "unblock",
            "user": user,
            "reason": "Requested by " + sendernick + " Reason: " + reason,
            "token": CSRF_TOKEN,
            "format": "json"
        }

        try:
            R = S.post(URL, data=PARAMS_3)
            DATA = R.json()
            bot.send_message(channel, "Unblock request sent. You may want to check https://" + wiki + ".miraheze.org/wiki/Special:Log?type=block&page=" + user + " to confirm that the unblock worked.")
        except:
            bot.send_message(channel, "An unexpected error occured. Did you type the wiki or user incorrectly? Do I have admin rights on that wiki?")
            
            
    if message.lower().startswith('!delete') and sender in stewards:
        
        arg = message.split(' ')
        if len(arg) == 3:
            wiki = arg[1]
            page = arg[2]
            reason = arg[3]
        elif len(arg) > 3:
            wiki = arg[1]
            page = arg[2]
            reason = message.split(user, 1)[1]
        else:
            bot.send_message(channel, "Syntax is !delete <wiki> <page> <reason>")
            return
        
        S = requests.Session()

        URL = "https://" + wiki + ".miraheze.org/w/api.php"
        PARAMS_0 = {
            "action": "query",
            "meta": "tokens",
            "type": "login",
            "format": "json"
        }
        try:
             R = S.get(url=URL, params=PARAMS_0)
             DATA = R.json()
        except:
             bot.send_message(channel, "Catostrophic Error! Unable to connect to the wiki.")
             return

        LOGIN_TOKEN = DATA['query']['tokens']['logintoken']
        
        PARAMS_1 = {
         "action": "login",
         "lgname": "EkWikiBot",
         "lgpassword": nonflagpass,
         "lgtoken": LOGIN_TOKEN,
         "format": "json"
        }

        try:
             R = S.post(URL, data=PARAMS_1)
        except:
            bot.send_message(channel, "Catostrophic Error! Unable to connect to the wiki.")
            return

        PARAMS_2 = {
            "action": "query",
            "meta": "tokens",
            "format": "json"
        }

        try:
             R = S.get(url=URL, params=PARAMS_2)
             DATA = R.json()
        except:
            bot.send_message(channel, "Catostrophic Error! Unable to connect to the wiki.")
            return

        CSRF_TOKEN = DATA['query']['tokens']['csrftoken']
        
        PARAMS_3 = {
            'action': "delete",
            'title': page,
            'reason': "Requested by " + sender + " Reason: " + reason,
            'token': CSRF_TOKEN,
            'format': "json"
        }

        try:
         R = S.post(URL, data=PARAMS_3)
         DATA = R.json()
         bot.send_message(channel, "The delete request was sent. You should check the wiki to make sure the page was deleted.")
        except:
         bot.send_message(channel, "An unexpected error occured. Did you type the wiki or page incorrectly? Do I have admin rights on that wiki?")

    if message.lower().startswith('!log') and sender in stewards:
        
        arg = message.split(' ')
        if len(arg) == 1:
            message = arg[1]
        elif len(arg) > 1:
            reason = message.split('!log', 1)[1]
        else:
            bot.send_message(channel, "Syntax is !log <message>")
            return
        
        S = requests.Session()

        URL = "https://test.miraheze.org/w/api.php"

# Step 1: GET request to fetch login token
        PARAMS_0 = {
            "action": "query",
            "meta": "tokens",
            "type": "login",
            "format": "json"
        }

        try:
            R = S.get(url=URL, params=PARAMS_0)
            DATA = R.json()
        except:
            bot.send_message(channel, "Catostrophic Error! Unable to connect to the wiki.")
            return

        LOGIN_TOKEN = DATA['query']['tokens']['logintoken']

# Step 2: POST request to log in. Use of main account for login is not
# supported. Obtain credentials via Special:BotPasswords
# (https://www.mediawiki.org/wiki/Special:BotPasswords) for lgname & lgpassword
        PARAMS_1 = {
        "action": "login",
        "lgname": "EkWikiBot",
        "lgpassword": flagpass,
        "lgtoken": LOGIN_TOKEN,
        "format": "json"
        }
        try:
            R = S.post(URL, data=PARAMS_1)
        except:
            bot.send_message(channel, "Catostrophic Error! Unable to connect to the wiki.")
            return

# Step 3: GET request to fetch CSRF token
        PARAMS_2 = {
            "action": "query",
            "meta": "tokens",
            "format": "json"
        }

        try:
            R = S.get(url=URL, params=PARAMS_2)
            DATA = R.json()
        except:
            bot.send_message(channel, "Catostrophic Error! Unable to connect to the wiki.")
            return

        CSRF_TOKEN = DATA['query']['tokens']['csrftoken']

# Step 4: POST request to block user
        PARAMS_3 = {
            "action": "edit",
            "title": "TestLogPage",
            "summary": message + "(" + sender + ")",
            "appendtext": "\n* " + sender + ": " + message,
            "token": CSRF_TOKEN,
            "bot": "true",
            "format": "json"
        }

        try:
            R = S.post(URL, data=PARAMS_3)
            DATA = R.json()
            bot.send_message(channel, "Logged message at https://test.miraheze.org/wiki/TestLogPage")
        except:
            bot.send_message(channel, "An unexpected error occured. Do I have edit rights on that wiki?")
        
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
