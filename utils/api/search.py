from utils.api import fetch_from_api
from datetime import datetime
from utils.api.scoring import score_videos
from utils.mysql.get import get_videos
from utils.mysql.connect import get_mysql


def get_published_datetime(published):
    return datetime.strptime(published, "%Y-%m-%dT%H:%M:%SZ")


def search(query, pages=1, max=50, starting_token='', threshold=0.0):
    s = []

    counts = {}

    if starting_token == '':
        s = fetch_from_api.search_videos(query, pages, max)
    else:
        s = fetch_from_api.search_videos(query, pages, max, starting_token)

    # print('{} videos fetched'.format(len(s)))
    counts['API'] = len(s)

    not_exists = []

    video_data = get_videos(get_mysql(), from_flask=False)
    video_ids = list(map(lambda x: x['video_id'], video_data))

    for v in s:
        if v['video_id'] not in video_ids:
            # if not video_exists(get_mysql(), v['video_id'], from_flask=False):
            not_exists.append(v)

    # print('{} not already existing videos found'.format(len(not_exists)))
    counts['non-existing'] = len(not_exists)

    scores = score_videos(not_exists, search_tags=False)

    videos_json = {}

    # print('Fetching extended data and filtering by score (threshold={})... '.format(threshold), end='')
    for v in not_exists:
        if scores[v['video_id']] > threshold:
            details = fetch_from_api.get_video_by_id(v['video_id'])
            videos_json[v['video_id']] = details
        else:
            print('Filtered Out (1): {}\t{}'.format(v['video_id'], v['video_title']))

    #print('{} videos after filter'.format(len(videos_json)))
    counts['filter 1'] = len(videos_json)

    print('---Stats---')

    for k, v in counts.items():
        print('{}: {}'.format(k, v))

    return videos_json
