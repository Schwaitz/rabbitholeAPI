import json
from datetime import datetime
import YoutubeAPI

import app_config as app_config

from utils.mysql.execute import *
from utils.mysql.get import *


def make_response(status, message):
    response_data = {
        'status': status,
        'message': message
    }
    return json.dumps(response_data)


def make_success(message):
    return make_response('success', message)


def make_fail(message):
    return make_response('fail', message)


def make_error(message):
    return make_response('error', message)


def already_exists_error(category):
    return make_fail(category + ' already exists')


def does_not_exist_error(category):
    return make_fail(category + ' does not exist')


def create_channel(mysql, channel, check_exists=True):
    if check_exists:
        if channel_exists(mysql, channel['channel_id']):
            return already_exists_error('Channel')

    data = execute_insert(mysql, 'channels', ['channel_id', 'channel_title', 'channel_description', 'channel_thumbnail_url', 'channel_uploads_playlist'],
                          (channel['channel_id'], channel['channel_title'], channel['channel_description'], channel['channel_thumbnail_url'], channel['channel_uploads_playlist']))
    return json.dumps(data)


def create_channel_by_id(mysql, channel_id):
    if not channel_exists(mysql, channel_id):
        channel = YoutubeAPI.get_channel_by_id(channel_id)
        create_channel(mysql, channel, False)


def create_video(mysql, video, check_exists=True):
    if check_exists:
        if video_exists(mysql, video['video_id']):
            return already_exists_error('Video')

    if not channel_exists(mysql, video['channel_id']):
        res = create_channel(mysql, video['channel_id'])
        print("Channel Created: " + str(res))
    else:
        pass
        # print("Channel Exists, Skipping")

    print("Inserting video " + video['video_id'])
    data = execute_insert(mysql, 'videos',
                          ['video_id', 'video_title', 'video_description', 'video_thumbnail_url', 'video_published_date',
                           'video_views', 'video_likes', 'video_dislikes', 'video_comments', 'video_channel_hm', 'video_tags'],
                          (video['video_id'], video['video_title'], video['video_description'], video['video_thumbnail_url'], get_published_datetime(video['video_published_date']),
                           video['video_views'], video['video_likes'], video['video_dislikes'], video['video_comments'], get_channel_hm_from_id(video['channel_id']),
                           json.dumps(video['video_tags'])))
    return json.dumps(data)


def create_video_by_id(mysql, video_id):
    if not video_exists(mysql, video_id):
        video = YoutubeAPI.get_video_by_id(video_id)

        create_video(mysql, video, False)


def create_talent(mysql, talent_name, check_exists=True):
    if check_exists:
        if talent_exists(mysql, talent_name):
            return already_exists_error('Talent')

    print("Creating talent with name " + talent_name)
    data = execute_insert(mysql, 'talents', ['name'], [talent_name])
    return json.dumps(data)


def create_alias(mysql, alias, talent_name):
    if talent_exists(mysql, talent_name):
        if not alias_exists(mysql, alias):
            # print("Creating alias with name " + alias + " for " + talent_name)
            data = execute_insert(mysql, 'aliases', ['alias', 'talent_name'], [alias, talent_name])
            return json.dumps(data)

        else:
            already_exists_error('Alias')

    else:
        return does_not_exist_error('Talent')
