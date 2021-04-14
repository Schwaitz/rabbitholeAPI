from datetime import datetime
import json


def get_published_datetime(published):
    return datetime.strptime(published, "%Y-%m-%dT%H:%M:%SZ")

def get_timestamp():
    return str(datetime.now().strftime("%m-%d-%y %H-%M-%S"))

def convert(data):
    videos = []

    for k, v in data.items():
        videos.append({
            "video_channel_hm": "http://api/rabbithole.moe/channels/" + data[k]['channelId'],
            "video_comments": data[k]['comments'],
            "video_description": data[k]['description'],
            "video_dislikes": data[k]['dislikes'],
            "video_id": k,
            "video_likes": data[k]['likes'],
            "video_player": "",
            "video_published_date": get_published_datetime(data[k]['published']),
            "video_tags": json.dumps(data[k]['tags']),
            "video_thumbnail_url": data[k]['thumbnail'],
            "video_title": data[k]['title'],
            "video_views": data[k]['views']
        })

    return videos


def read_json(file_name):
    file = open(file_name, 'r', encoding='utf-8')
    data = json.loads(file.read())
    file.close()

    return data


def write_json(identifier, to_write, timestamp=True):
    file = open(identifier + '-' + get_timestamp() + '.json', 'w+', encoding='utf-8')
    file.write(json.dumps(to_write))
    file.close()



