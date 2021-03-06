import json

from utils.api.fetch_from_api import *

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


def create_channel(mysql, channel, check_exists=True, from_flask=True):
    if check_exists:
        if channel_exists(mysql, channel['channel_id'], from_flask=from_flask):
            return already_exists_error('Channel')

    data = execute_insert(mysql, 'channels', ['channel_id', 'channel_title', 'channel_description', 'channel_thumbnail_url', 'channel_uploads_playlist'],
                          (channel['channel_id'], channel['channel_title'], channel['channel_description'], channel['channel_thumbnail_url'], channel['channel_uploads_playlist']),
                          from_flask=from_flask)
    return json.dumps(data)


def create_channel_by_id(mysql, channel_id, from_flask=True):
    if not channel_exists(mysql, channel_id, from_flask=from_flask):
        channel = get_channel_by_id(channel_id)
        create_channel(mysql, channel, False, from_flask=from_flask)


def create_video(mysql, video, check_exists=True, from_flask=True):
    if check_exists:
        if video_exists(mysql, video['video_id'], from_flask=from_flask):
            return already_exists_error('Video')

    if not channel_exists(mysql, video['channel_id'], from_flask=from_flask):
        res = create_channel_by_id(mysql, video['channel_id'], from_flask=from_flask)
        # print("Channel Created: " + str(res))
    else:
        pass
        # print("Channel Exists, Skipping")

    # print("Inserting video " + video['video_id'])

    key_list = ['video_likes', 'video_dislikes', 'video_comments']

    for k in key_list:
        if video[k] == 'N/A':
            video[k] = 0

    data = execute_insert(mysql, 'videos',
                          ['video_id', 'video_title', 'video_description', 'video_thumbnail_url', 'video_published_date',
                           'video_views', 'video_likes', 'video_dislikes', 'video_comments', 'video_channel_hm', 'video_tags'],
                          (video['video_id'], video['video_title'], video['video_description'], video['video_thumbnail_url'], get_published_datetime(video['video_published_date']),
                           video['video_views'], video['video_likes'], video['video_dislikes'], video['video_comments'], get_channel_hm_from_id(video['channel_id']),
                           json.dumps(video['video_tags'])), from_flask=from_flask)
    return json.dumps(data)


def create_video_by_id(mysql, video_id, from_flask=True):
    if not video_exists(mysql, video_id, from_flask=from_flask):
        video = get_video_by_id(video_id)

        create_video(mysql, video, False, from_flask=from_flask)


def create_talent(mysql, talent_name, check_exists=True, from_flask=True):
    if check_exists:
        if talent_exists(mysql, talent_name, from_flask=from_flask):
            return already_exists_error('Talent')

    print("Creating talent with name " + talent_name)
    data = execute_insert(mysql, 'talents', ['name'], [talent_name], from_flask=from_flask)
    return json.dumps(data)


def create_alias(mysql, alias, talent_name, from_flask=True):
    if talent_exists(mysql, talent_name, from_flask=from_flask):
        if not alias_exists(mysql, alias, from_flask=from_flask):
            # print("Creating alias with name " + alias + " for " + talent_name)
            data = execute_insert(mysql, 'aliases', ['alias', 'talent_name'], [alias, talent_name], from_flask=from_flask)
            return json.dumps(data)

        else:
            already_exists_error('Alias')

    else:
        return does_not_exist_error('Talent')


def create_entry(mysql, video, talent, check_exists=True, from_flask=True):
    if check_exists:
        if entry_exists(mysql, video=video, talent=talent, from_flask=from_flask):
            return_error = already_exists_error('Entry')
            print('fail: entry for {} with id {}'.format(talent, video))
            return return_error

    data = execute_insert(mysql, 'entries', ['video', 'talent'], [video, talent], from_flask=from_flask)
    print('{}: entry for {} with id {}'.format(data['status'], talent, video))

    return json.dumps(data)




