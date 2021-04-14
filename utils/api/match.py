import re
from utils.data.common import *
from utils.data.globals import holo_related_keywords, translation_keywords

collab_keywords = [
    'collab',
    'th gen',
    'st gen',
    'all pov',
    'everyone',
    'compilation',
    'hololive members',
    'holostars members',
    'hololive girls'
]

collab_override_keywords = [
    'sports festival',
    'among us',
    'amongus',
    'hololive en rewind',
    'hololiveen clip dump'
]

collab_additional_keywords = [
    'hololiveen',
    'hololive en',
    'minecraft',
    'reacts',
    'reaction',
    'no context'
]

talent_data = get_talents()
matches = {}
videos_for_name = {}
is_matched = {}
name_match_list = {}
collab_ids = []

all_keywords = holo_related_keywords + translation_keywords


def keyword_search(word, text, use_regex=True):
    if use_regex:
        return re.search(rf"\b{word.lower()}(?:\b|s)", text.lower())
    else:
        return word in text.lower()


def name_matches(v, unique_matches_only=False):
    match_list = {
        'unique': 0,
        'keyword': 0,
        'matches': [],
        'unique_matches': [],
        'location': 'N/A',
        'collab': False,
        'collab keyword': 'N/A'
    }
    full_name_match_list = []

    for name, aliases in talent_data.items():
        found_name = False

        name_no_spaces = name.replace(' ', '').lower()
        name_and_aliases = [name_no_spaces] + aliases

        for a in name_and_aliases:
            if keyword_search(a, v['video_title']):
                if not found_name:
                    full_name_match_list.append(name)
                    match_list['unique'] += 1
                    match_list['location'] = 'title'
                    match_list['unique_matches'].append(name)
                    found_name = True

                match_list['keyword'] += 1
                match_list['matches'].append(a)

                if unique_matches_only:
                    break

    if not match_list['matches']:
        for name, aliases in talent_data.items():
            found_name = False

            name_no_spaces = name.replace(' ', '').lower()
            name_and_aliases = [name_no_spaces] + aliases

            for a in name_and_aliases:
                if keyword_search(a, v['video_description']):
                    if not found_name:
                        full_name_match_list.append(name)
                        match_list['unique_matches'].append(name)
                        found_name = True

                    match_list['matches'].append(a)

        if len(full_name_match_list) > 0:
            if len(full_name_match_list) <= 4:
                match_list['location'] = 'description'

                for t in match_list['matches']:
                    match_list['keyword'] += 1

                for t in full_name_match_list:
                    match_list['unique'] += 1

            else:
                match_list['unique'] = 0
                match_list['matches'] = []
                full_name_match_list = []
                match_list['location'] = 'N/A'
                # print('too many matches ({}): {} - {}'.format(len(full_name_match_list), v['video_id'], v['video_title']))

    found_collab = False
    found_keyword = ''
    for k in collab_keywords:
        if k in v['video_title'].lower():
            keywords_without = collab_keywords.copy()
            keywords_without.remove(k)

            if any(word in v['video_title'].lower() for word in keywords_without):
                found_collab = True
                found_keyword = k
                break
            if len(full_name_match_list) > 1:
                found_collab = True
                found_keyword = k
                break
            elif any(word in v['video_title'].lower() for word in collab_additional_keywords):
                found_collab = True
                found_keyword = k
                break
            else:
                # print('not found collab: {} - {}'.format(v['video_id'], v['video_title']))
                pass

    if not found_collab:
        for k in collab_override_keywords:
            if k in v['video_title'].lower():
                found_collab = True
                found_keyword = k
                break

    if found_collab:
        match_list['collab'] = True
        match_list['collab keyword'] = found_keyword

    return match_list


def talent_match(name, aliases, v):
    name_no_spaces = name.replace(' ', '').lower()
    name_and_aliases = [name_no_spaces] + aliases

    for a in name_and_aliases:
        if len(a) > 3:
            if keyword_search(a, v['video_title']):
                return True
        else:
            if keyword_search(a, v['video_title']):
                if any(keyword in v['video_title'].lower() for keyword in all_keywords):
                    return True
    return False


def get_talent_matches(v):
    matches = []

    for name, aliases in talent_data.items():
        name_no_spaces = name.replace(' ', '').lower()
        name_and_aliases = [name_no_spaces] + aliases

        for a in name_and_aliases:
            if len(a) > 3:
                if keyword_search(a, v['video_title']):
                    matches.append(name)
                    break
            else:
                if keyword_search(a, v['video_title']):
                    if any(keyword in v['video_title'].lower() for keyword in all_keywords):
                        matches.append(name)
                        break

    return matches


def any_talent_match(v):
    for name, aliases in get_talents().items():
        if talent_match(name, aliases, v):
            return True

    return False
