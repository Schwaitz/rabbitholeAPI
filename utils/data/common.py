import requests



def request_get_videos():
    return requests.get('http://api.rabbithole.moe/videos').json()

def request_get_channels():
    return requests.get('http://api.rabbithole.moe/channels').json()

def get_talents():
    return requests.get('http://api.rabbithole.moe/talents').json()