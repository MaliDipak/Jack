from flask import Flask, request, jsonify
from datetime import datetime
import wikipedia
import json
import random
import pyttsx3
import threading
import webbrowser
from googleapiclient.discovery import build

# Creating flask object
app = Flask(__name__)

# Loading Intents
f = open('My_Intents.json')

Intent = json.load(f)

# Closing file
f.close()


def speak(audio):
    # Generating voice
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.say(audio)
    engine.runAndWait()
    engine = None

    return


def get_system_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    response = {
        'fulfillmentText': "Current time is {}".format(current_time)
    }

    return response


def make_wikipedia_search(data):
    result = "Hello :)"
    key = data['queryResult']['parameters']['any']
    try:
        result = wikipedia.summary(str(key)+" Wikipedia", sentences=2)
    except:
        result = "I am not able to search "+key

    response = {
        'fulfillmentText': "According to wikipedia; {}".format(result)
    }

    return response


def play_youtube_video(data):
    key = data['queryResult']['parameters']['music-artist']
    # Enter your API key here
    API_KEY = 'AIzaSyASy28G4tbxOvr5UcXeAqfwzRTayMfvRO8'

    # Set the search query to use
    query = key

    if (key == ""):
        query = "Shri Hari Stostram"

    # Set the maximum number of results to return (up to 50)
    max_results = 1

    # Set the YouTube Data API version to use
    api_version = 'v3'

    # Set the name of the API service to use
    service_name = 'youtube'

    # Set the fields to return in the API response
    fields = 'items(id(videoId),snippet(publishedAt,channelId,channelTitle,title,description))'

    # Build the API service
    service = build(service_name, api_version, developerKey=API_KEY)

    # Make the API request to search for videos
    request = service.search().list(
        part='id,snippet',
        type='video',
        q=query,
        maxResults=max_results,
        fields=fields
    )
    response = request.execute()

    # Get the video ID of the first video
    video_id = response['items'][0]['id']['videoId']

    # Get the URL of the first video
    url = 'https://www.youtube.com/watch?v=' + video_id

    # Open the URL in the default web browser

    webbrowser.open(url)

    intent_name = data['queryResult']['intent']['displayName']

    l1 = Intent[intent_name]

    r = random.choice(l1)

    response = {
        'fulfillmentText': '{}'.format(r)
    }

    return response


@app.route("/", methods=['POST'])
def index():
    data = request.get_json()
    intent_name = data['queryResult']['intent']['displayName']
    response = "error"
    if (intent_name == 'time'):
        response = get_system_time()
    elif (intent_name == 'wikipedia'):
        response = make_wikipedia_search(data)
    elif (intent_name == 'play-yt-vm'):
        response = play_youtube_video(data)
    else:
        # print(intent_name)
        # print(Intent[intent_name])
        l1 = Intent[intent_name]

        r = random.choice(l1)

        response = {
            'fulfillmentText': '{}'.format(r)
        }

    # For testing purpose...
    r1 = response['fulfillmentText']
    response = {
        'fulfillmentText': "Server says: {}".format(r1)
    }

    t1 = threading.Thread(target=speak, args=(response['fulfillmentText'],))
    # To Say
    t1.start()

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
