from datetime import datetime

import app_config as app_config

from utils.mysql.execute import execute_select


def get_channels(mysql, from_flask=True):
    data = execute_select(mysql, """SELECT * FROM channels""", from_flask=from_flask)
    return data


def get_videos(mysql, from_flask=True):
    data = execute_select(mysql, """SELECT * FROM videos""", from_flask=from_flask)
    return data


def channel_exists(mysql, channel_id, from_flask=True):
    data = execute_select(mysql, """SELECT COUNT(*) FROM channels WHERE channel_id = %s""", (channel_id,), from_flask=from_flask)
    return data["COUNT(*)"] >= 1


def video_exists(mysql, video_id, from_flask=True):
    data = execute_select(mysql, """SELECT COUNT(*) FROM videos WHERE video_id = %s""", (video_id,), from_flask=from_flask)
    return data["COUNT(*)"] >= 1


def talent_exists(mysql, talent_name, from_flask=True):
    data = execute_select(mysql, """SELECT COUNT(*) FROM talents WHERE name = %s""", (talent_name,), from_flask=from_flask)
    return data["COUNT(*)"] >= 1


def alias_exists(mysql, alias, from_flask=True):
    data = execute_select(mysql, """SELECT COUNT(*) FROM aliases WHERE alias = %s""", (alias,), from_flask=from_flask)
    return data["COUNT(*)"] >= 1


def entry_exists(mysql, video='', talent='', from_flask=True):
    data = execute_select(mysql, """SELECT COUNT(*) FROM entries WHERE video = %s AND talent=%s""", (video, talent,), from_flask=from_flask)
    return data["COUNT(*)"] >= 1


def get_aliases_from_talent(mysql, talent_name, from_flask=True):
    data = execute_select(mysql, """SELECT * FROM aliases WHERE talent_name = %s""", (talent_name,), from_flask=from_flask)
    data_type = type(data)

    if data:
        aliases = []
        if data_type is list:
            for d in data:
                aliases.append(d['alias'])
        else:
            aliases.append(data['alias'])
    else:
        return []

    return aliases


def get_talent_from_alias(mysql, alias, from_flask=True):
    data = execute_select(mysql, """SELECT * FROM aliases WHERE alias = %s""", (alias,), from_flask=from_flask)
    if data:
        return data['talent_name']
    else:
        return ''


def get_talent(mysql, word, from_flask=True):
    talent_name = get_talent_from_alias(mysql, word.lower(), from_flask=from_flask)
    data = get_aliases_from_talent(mysql, talent_name, from_flask=from_flask)

    if data:
        return_data = {
            'name': talent_name,
            'aliases': data
        }

        return return_data
    else:
        return {}


def get_talents(mysql, from_flask=True, include_collab=False):
    data = execute_select(mysql, """SELECT * FROM talents""", from_flask=from_flask)

    talents = []
    for d in data:
        if d['name'] != 'collab':
            talents.append(d['name'])
        else:
            if include_collab:
                talents.append(d['name'])

    return talents


def get_aliases(mysql, from_flask=True):
    data = execute_select(mysql, """SELECT * FROM aliases""", from_flask=from_flask)
    return data


def get_videos_for_talent(mysql, talent, from_flask=True):
    data = execute_select(mysql, """SELECT videos.* FROM videos JOIN entries ON videos.video_id = entries.video WHERE entries.talent = %s""", (talent,), from_flask=from_flask)

    if not type(data) is list:
        return [data]
    else:
        return data


def get_talents_for_video(mysql, video, from_flask=True):
    data = execute_select(mysql, """SELECT talents.* FROM talents JOIN entries ON talents.name = entries.talent WHERE entries.video = %s""", (video,), from_flask=from_flask)

    if not type(data) is list:
        return [data]
    else:
        return data


def get_channel_hm_from_id(channel_id):
    return app_config.url_host + '/channels/' + channel_id


def get_video_hm_from_id(video_id):
    return app_config.url_host + '/videos/' + video_id


def get_published_datetime(published):
    temp = datetime.strptime(published, "%Y-%m-%dT%H:%M:%SZ")
    return temp.strftime('%Y-%m-%d %H:%M:%S')
