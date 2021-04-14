from utils.api.search import search
from utils.api.scoring import *
from utils.data.json_manipulation import *
from datetime import datetime
import os

from utils.mysql.create import create_video
from utils.mysql.connect import get_mysql


def get_data_from_api(query, pages=1, max=50, starting_token='', threshold=0.0):
    videos = search(query, pages, max, starting_token, threshold)

    filtered = filter_videos_by_score(videos)

    now = str(datetime.now().strftime("%m-%d-%y %H-%M-%S"))
    if not os.path.exists('./logs/' + now):
        os.makedirs('./logs/' + now)

    write_json('./logs/{}/filtered-{})'.format(now, len(filtered)), filtered, timestamp=False)

    print('filter 2: {}'.format(len(filtered)))

    log_data = {
        'stats': {
            'search': {
                'query': query,
                'pages': pages,
                'max': max,
                'starting_token': starting_token,
                'threshold': threshold
            },
            'filtered': len(filtered)
        },
        'data': {}
    }

    for v in filtered:
        log_data['data'][v['video_id']] = {
            'success': False,
            'data': v,
            'result': {}
        }

    success_count = 0

    for v in filtered:
        try:
            print('Inserting {}... '.format(v['video_id']), end='')
            r = json.loads(create_video(get_mysql(), v, from_flask=False))

            if r['status'] == 'success':
                r_min = r.copy()
                del r_min['data']

                success_count += 1
                log_data['data'][v['video_id']]['success'] = True
                log_data['data'][v['video_id']]['result'] = r_min
            else:
                print('failed')

            print(str(r))
        except:
            print('exception')



    write_json('./logs/{}/fetched ({} of {})'.format(now, success_count, len(filtered)), log_data, timestamp=False)




def get_data_from_json(file_name):
    videos = read_json(file_name)

    for v in videos:
        print('Inserting {}... '.format(v['video_id']), end='')
        r = create_video(get_mysql(), v, from_flask=False)
        print(str(r))

    # get_data_from_api('"hololiveID" clip', 5, 50)

    # get_data_from_json('./json/search-04-13-21 19-49-55.json')
