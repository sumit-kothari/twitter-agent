from flask import Flask
from flask import render_template, redirect
from flask import request as flask_request
import tweepy
import apiai
from langdetect import detect
import json
import logging


logging.basicConfig(filename='file.log',level=logging.DEBUG)


CONSUMER_KEY = "<CONSUMER_KEY>"
CONSUMER_SECRET = "<CONSUMER_SECRET>"
ACCESS_TOKEN = "<ACCESS_TOKEN>"
ACCESS_TOKEN_SECRET = "<ACCESS_TOKEN_SECRET>"
APIAI_CLIENT_ACCESS_TOKEN = "<APIAI_CLIENT_ACCESS_TOKEN>"


app = Flask(__name__)

@app.route('/')
def indexRoute():
    return render_template('root.html')


def _twitterTest(username):

    logging.info("Twitter username requested = %s", username) 

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)

    tweetText = ""

    public_tweets = api.user_timeline(screen_name = username, count=1)

    logging.info("Twitter api response = %s", public_tweets) 

    for tweet in public_tweets:
        tweetText = tweet.text
        logging.info("Twitter api response tweetText = %s", tweetText) 

    return {
        "status" : True,
        "message" : tweetText
    }


@app.route('/api_ai_test', methods=['POST'])
def apiAiTEst():

    requestData = flask_request.json

    logging.info("requestData = %s", requestData) 

    if requestData["query"]:

        logging.info("requestData query= %s", requestData["query"]) 

        ai = apiai.ApiAI(APIAI_CLIENT_ACCESS_TOKEN)

        request = ai.text_request()

        request.session_id = "1234567890"

        request.query = requestData["query"]

        response = request.getresponse()
        response = json.loads(response.read().decode('utf-8'))

        logging.info("apiai response= %s", response) 


        if response["result"]["metadata"]["intentName"] == "tweet-search":
            logging.info("apiai intentName= %s", response["result"]["metadata"]["intentName"]) 

            returnData = _twitterTest(response["result"]["parameters"]["any"])
        else:
            logging.warn("apiai intentName is default") 
            returnData = {
                "status" : False,
                "message" : "Please try again, search tweets like : 'Tweet of narendramodi" 
            }
    else:

        logging.error("Invalid params in query") 

        returnData = {
            "status" : False,
            "message" : "Some error occurred, search tweets like : 'Tweet of narendramodi" 
        }   

    return json.dumps(returnData)


@app.errorhandler(404)
def page_not_found(e):
    return redirect("/")


@app.route('/detect_lang')
def detectLang(): 

    output = detect("Ein, zwei, drei, vier")
    print(output)

    return "ok"    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)