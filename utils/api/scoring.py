import requests
import json
from datetime import datetime
import app_config as app_config
from utils.data.globals import *
from utils.data.common import get_talents
import re


tag_keywords = []

count = 0


talent_data = get_talents()

def score_videos(videos, search_tags=True):
    def calc_name_score(category):
        amount = name_worth[category] * (1 - (name_counts[category] * name_count_exponent[category]))

        if amount < 0:
            return 0
        else:
            return amount

    def keyword_exists(v, words, check_title=True, check_description=True, check_tags=True):

        tags_string = ''
        if check_tags:
            tags = list(v['video_tags'])
            tags_lower = list(map(lambda x: x.lower(), tags))
            tags_string = ' '.join(tags_lower)

        if check_title:
            if any(re.search(rf"\b{t}\b", v['video_title'].lower()) for t in words):
                return True

        if check_description:
            if any(re.search(rf"\b{t}\b", v['video_description'].lower()) for t in words):
                return True

        if check_tags:
            if any(re.search(rf"\b{t}\b", tags_string) for t in words):
                return True

        return False

    name_title_matches = 0
    name_description_matches = 0
    name_tag_matches = 0

    to_remove = []
    to_remove_json = []

    scores = {}

    for vid in videos:
        v = vid

        if search_tags:
            v = videos[vid]

        holo_related_exists = keyword_exists(v, holo_related_keywords, check_tags=search_tags)
        score = 0.0

        channel_id = ''
        if 'channel_id' in v.keys():
            channel_id = v['channel_id']
        else:
            channel_id = v['video_channel_hm'][-24:]

        found_names = {}

        name_counts = {
            "title": 0,
            "description": 0,
            "tags": 0
        }

        matches = {
            "hololive": False,
            "vtuber": False,
            "translation": False
        }

        tags_string = ''

        if search_tags:
            tags = list(v['video_tags'])
            tags_lower = list(map(lambda x: x.lower(), tags))
            tags_string = ' '.join(tags_lower)

        for talent_name, aliases in talent_data.items():
            filtered_aliases = list(filter(lambda x: (len(x) > 3), aliases))
            short_aliases = list(set(aliases) - set(filtered_aliases))

            if re.search(rf"\b{talent_name}\b", v['video_title'].lower()) or any(re.search(rf"\b{alias}\b", v['video_title'].lower()) for alias in filtered_aliases):
                category = 'title'
                score += calc_name_score(category)
                name_counts[category] += 1
                name_title_matches += 1
                found_names[talent_name] = True

            else:
                if len(short_aliases) > 0:
                    for a in short_aliases:
                        if re.search(rf"\b{a}\b", v['video_title'].lower()) and holo_related_exists:
                            category = 'title'
                            score += calc_name_score(category)
                            name_counts[category] += 1
                            name_title_matches += 1
                            found_names[talent_name] = True

                            # print("!!!Title Short Alias {} granted on {}".format(a, v['video_title']))

            if re.search(rf"\b{talent_name}\b", v['video_description'].lower()) or any(re.search(rf"\b{alias}\b", v['video_description'].lower()) for alias in filtered_aliases):
                category = 'description'
                score += calc_name_score(category)
                name_counts[category] += 1
                name_description_matches += 1
                found_names[talent_name] = True

            else:
                if len(short_aliases) > 0:
                    for a in short_aliases:
                        if re.search(rf"\b{a}\b", v['video_description'].lower()) and holo_related_exists:
                            category = 'description'
                            score += calc_name_score(category)
                            name_counts[category] += 1
                            name_title_matches += 1
                            found_names[talent_name] = True

                            # print("!!!Description Short Alias {} granted on {}".format(a, v['video_title']))

            if search_tags:
                if re.search(rf"\b{talent_name}\b", tags_string) or any(re.search(rf"\b{alias}\b", tags_string) for alias in filtered_aliases):
                    category = 'tags'
                    score += calc_name_score(category)
                    name_counts[category] += 1
                    name_tag_matches += 1
                    found_names[talent_name] = True

                else:
                    if len(short_aliases) > 0:
                        for a in short_aliases:
                            if re.search(rf"\b{a}\b", tags_string) and holo_related_exists:
                                category = 'tags'
                                score += calc_name_score(category)
                                name_counts[category] += 1
                                name_title_matches += 1
                                found_names[talent_name] = True

        name_count_sum = name_counts['title'] + name_counts['description']

        if search_tags:
            name_count_sum += name_counts['tags']

        if name_count_sum > 1:
            for k in keywords:
                if any(t in v['video_title'].lower() for t in k['list']):
                    score += k['worth']['title']
                    matches[k['category']] = True

                if any(t in v['video_description'].lower() for t in k['list']):
                    score += k['worth']['description']
                    matches[k['category']] = True

                if search_tags:
                    if any(t in tags_string for t in k['list']):
                        score += k['worth']['tags']
                        matches[k['category']] = True

        if name_count_sum > 1 or holo_related_exists:
            if any(t in v['video_title'].lower() for t in translation_keywords):
                score += translation_worth['title']

                if holo_related_exists:
                    score += 5.0

            if any(t in v['video_description'].lower() for t in translation_keywords):
                score += translation_worth['description']

            if search_tags:
                if any(t in tags_string for t in translation_keywords):
                    score += translation_worth['tags']

        # Disqualifiers

        if name_count_sum == 0 and keyword_exists(v, no_name_blacklist, check_tags=search_tags):
            score = -1.0

        if channel_id in official_channels_blacklist or channel_id in manual_channel_blacklist:
            score = -1.0

        if v['video_id'] in manual_video_blacklist:
            score = -1.0

        # Videos about actual festivals
        if len(found_names) == 1 and 'Natsuiro Matsuri' in found_names.keys():
            if not keyword_exists(v, ['natsuiro', 'matsuri\'s'] + holo_related_keywords, check_tags=search_tags):
                score = -1.0

            elif not holo_related_exists and keyword_exists(v, ['Ume Matsuri', 'haikyuu']):
                score = -1.0

        if not holo_related_exists and keyword_exists(v, ['della luna', 'del luna'], check_tags=search_tags):
            score = -1.0

        if keyword_exists(v, ['live wallpaper'], check_description=False):
            score = -1.0

        # Subaru Outback
        if len(found_names) == 1 and 'Oozora Subaru' in found_names.keys():
            if keyword_exists(v, ['subaru outback'], check_tags=search_tags):
                score = -1.0

        scores[v['video_id']] = score

    return scores


def filter_videos_by_score(videos, threshold=10.0):
    scores = score_videos(videos)
    filtered = []

    for k, v in videos.items():
        if scores[k] >= threshold:
            videos[k]['score'] = scores[k]
            filtered.append(videos[k])
        else:
            pass
            # print('Filtered Out (2): {}\t{}'.format(v['video_id'], v['video_title']))

    return filtered
