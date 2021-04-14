import requests
import app_config as app_config


def request_get_videos():
    return requests.get('http://api.rabbithole.moe/videos').json()


def request_get_channels():
    return requests.get('http://api.rabbithole.moe/channels').json()


def get_talents():
    return requests.get('http://api.rabbithole.moe/talents').json()


def delete_by_id(id):
    r = requests.delete(app_config.url_host + '/videos/' + id).json()
    print(str(r))
