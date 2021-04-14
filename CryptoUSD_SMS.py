import array
import time
import schedule
from pycoingecko import CoinGeckoAPI
from twilio.rest import Client
from datetime import datetime
from twilio_info import account_sid, auth_token, twilioNum,toNum, receivingTime

#API Variables
cg = CoinGeckoAPI()
client = Client(account_sid, auth_token)


#dict/array for sorting user input
enteredCoins = {}
bodyArr = []


#send SMS
def sendSMS(body, toNum, fromNum):

    message = client.messages.create(
        body=str(body),
        from_=fromNum,
        to=str(toNum)
    )

    print(message.sid)


#Creates coin objects from which price data is pulled from
class MyCoin:
    def __init__(self, coinid):
        self.coinid = coinid
    def getValue(self):
        USD = cg.get_price(ids=self.coinid, vs_currencies='usd')
        return USD

#Allows users to input coins of choice
def coinEntry():
    coinNum = 0
    while True: 
        coinID = input ('Please enter your coin. When finished, please type "done":\n')
        coinInput = (str(coinID))
        if coinID == 'done':     
            break
            
        print("You entered " + coinID)
        enteredCoins[coinNum] = coinInput
        coinNum = coinNum + 1
    #loop through entered coins and pull their values from enteredCoins into an array that will be sent to users.
    for i in enteredCoins:
        co = str(enteredCoins.get(i))
        newCoin = MyCoin(co)
        bodyArr.append(newCoin.getValue())
    

 #function to be run daily by schedule       
def scheduledJob():
    body = '\n'.join(map(str, bodyArr))
    sendSMS(body,toNum, twilioNum)


def main():
    print("Welcome to the Cryptocurrency to USD SMS Notifier, using the CoinGecko API. \nPlease make sure you set you Twilio information, sending time, and the receiving phone number in twilio_info.py.\n")
    coinEntry()
    schedule.every().day.at(receivingTime).do(scheduledJob)
    
    #keeps application running indefinitely
    while True:
        schedule.run_pending()
        time.sleep(2)






main()



