import json
from datetime import datetime
import YoutubeAPI

import app_config as app_config

from utils.mysql.execute import execute_select


def get_channels(mysql):
    data = execute_select(mysql, """SELECT * FROM channels""")
    return data


def get_videos(mysql):
    data = execute_select(mysql, """SELECT * FROM videos""")
    return data


def channel_exists(mysql, channel_id):
    data = execute_select(mysql, """SELECT COUNT(*) FROM channels WHERE channel_id = %s""", (channel_id,))
    return data["COUNT(*)"] >= 1


def video_exists(mysql, video_id):
    data = execute_select(mysql, """SELECT COUNT(*) FROM videos WHERE video_id = %s""", (video_id,))
    return data["COUNT(*)"] >= 1


def talent_exists(mysql, talent_name):
    data = execute_select(mysql, """SELECT COUNT(*) FROM talents WHERE name = %s""", (talent_name,))
    return data["COUNT(*)"] >= 1


def alias_exists(mysql, alias):
    data = execute_select(mysql, """SELECT COUNT(*) FROM aliases WHERE alias = %s""", (alias,))
    return data["COUNT(*)"] >= 1


def get_aliases_from_talent(mysql, talent_name):
    data = execute_select(mysql, """SELECT * FROM aliases WHERE talent_name = %s""", (talent_name,))

    if data:
        aliases = []
        for d in data:
            aliases.append(d['alias'])

        return aliases
    else:
        return []


def get_talent_from_alias(mysql, alias):
    data = execute_select(mysql, """SELECT * FROM aliases WHERE alias = %s""", (alias,))
    if data:
        return data['talent_name']
    else:
        return ''


def get_talent(mysql, word):
    talent_name = get_talent_from_alias(mysql, word.lower())
    data = get_aliases_from_talent(mysql, talent_name)

    if data:
        return_data = {
            'name': talent_name,
            'aliases': data
        }

        return return_data
    else:
        return {}


def get_talents(mysql):
    data = execute_select(mysql, """SELECT * FROM talents""")

    talents = []
    for d in data:
        talents.append(d['name'])

    return talents


def get_aliases(mysql):
    data = execute_select(mysql, """SELECT * FROM aliases""")
    return data


def get_channel_hm_from_id(channel_id):
    return app_config.url_host + '/channels/' + channel_id


def get_video_hm_from_id(video_id):
    return app_config.url_host + '/videos/' + video_id


def get_published_datetime(published):
    temp = datetime.strptime(published, "%Y-%m-%dT%H:%M:%SZ")
    return temp.strftime('%Y-%m-%d %H:%M:%S')
