from flask import Flask, request, jsonify
from telegram_bot import TelegramBot
from config import TELEGRAM_INIT_WEBHOOK_URL
import requests,json,urllib.parse
import bs4
import time


app = Flask(__name__)
TelegramBot.init_webhook(TELEGRAM_INIT_WEBHOOK_URL)


@app.route('/')
def home():
    return "<h1>SAIRAJ INFO</h1>"


@app.route('/webhook', methods=['POST'])
def index():
    req = request.get_json() 
    bot = TelegramBot()
    bot.parse_webhook_data(req)
    
    if bot.incoming_message_text == '/start':
            message = 'Enter IDs in format--> /set seriesid-matchid '
            success=bot.send_msg(bot.chat_id,message)
            return jsonify(success=success)

    elif bot.incoming_message_text[0:4]=="/set":
            if bot.incoming_message_text[5:].strip(" ")==False:
                success=bot.send_msg(bot.chat_id,"please enter some text")
                return jsonify(success=success)
            
            sid=bot.incoming_message_text[5:12]
            mid=bot.incoming_message_text[13:]
            print(sid,mid)
            
            
            
            
            r = requests.get('https://hs-consumer-api.espncricinfo.com/v1/pages/match/home?seriesId='+sid+'&matchId='+mid)
            pdata=r.json()
            uid=pdata['content']['recentBallCommentary']['ballComments'][0]['_uid']
            while True:
                message=""
                r = requests.get('https://hs-consumer-api.espncricinfo.com/v1/pages/match/home?seriesId='+sid+'&matchId='+mid)
                pdata=r.json()
    
                if pdata['content']['recentBallCommentary']['ballComments'][0]['_uid']!=uid:
                    message+='\n'+pdata['match']['slug']
                    message+='\n'+pdata['match']['statusText']
                    message+='\n'+'Innings : '+str(pdata['match']['liveInning'])

                    if(pdata['match']['teams'][0]['inningNumbers'][0]==pdata['match']['liveInning']):
                        message+='\n'+pdata['match']['teams'][0]['team']['abbreviation']
                    else:message+='\n'+pdata['match']['teams'][1]['team']['abbreviation']
                    message+='\n'+str(pdata['content']['recentBallCommentary']['ballComments'][0]['oversActual'])

                    if(pdata['content']['recentBallCommentary']['ballComments'][0]['wides']!=0):
                        message+='\n'+'WIDE'
                    elif(pdata['content']['recentBallCommentary']['ballComments'][0]['noballs']!=0):
                        message+='\n'+'NO-BALL'

                    if(pdata['match']['status']=='RESULT'):
                        message+='\n'+pdata['match']['statusText']
                    elif(pdata['content']['recentBallCommentary']['ballComments'][0]['totalRuns']==4):
                        message+='\n'+'FOUR!!'
                    elif(pdata['content']['recentBallCommentary']['ballComments'][0]['totalRuns']==6):
                        message+='\n'+'SIX!!!'
                    elif(pdata['content']['recentBallCommentary']['ballComments'][0]['totalRuns']>0 and pdata['content']['recentBallCommentary']['ballComments'][0]['totalRuns']<4):
                        message+='\n'+str(pdata['content']['recentBallCommentary']['ballComments'][0]['totalRuns'])+' Runs!!'
                    elif(pdata['content']['recentBallCommentary']['ballComments'][0]['dismissalType']!=None):
                        message+='\n'+'WICKET!!!'
                        print(pdata['content']['recentBallCommentary']['ballComments'][0]['dismissalText']['commentary'])
                    elif(pdata['content']['recentBallCommentary']['ballComments'][0]['totalRuns']==0):
                        message+='\n'+'DOT!!!'
                    uid=pdata['content']['recentBallCommentary']['ballComments'][0]['_uid']
                    


                    print(str(message))
                    success=bot.send_msg(bot.chat_id,urllib.parse.quote(message))
                    time.sleep(2)
                    return jsonify(success=success)
                
    else:
            message = "invalid command"
            success=bot.send_msg(bot.chat_id,"Invalid Command")
            return jsonify(success=success) 

if __name__ == '__main__':
    app.run(host ='0.0.0.0',port=80)


# https://telegram.me

# check bot initialization: https://api.telegram.org/bot<secret key>/getme
# check webhook url: https://api.telegram.org/secret key/getWebhookInfo
