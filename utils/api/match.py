import re
from utils.data.common import *

holo_related_keywords = ['hololive', 'holo live', 'holoen', 'holo en', 'holoid', 'holo id', 'holostars', 'holo stars', 'hololiveclips', 'hololiveclip']
translation_keywords = ['engsub', 'eng sub', 'english sub', 'sub eng', 'holoengsubs']

all_keywords = holo_related_keywords + translation_keywords


def keyword_search(word, text, use_regex=True):
    if use_regex:
        return re.search(rf"\b{word.lower()}(?:\b|s)", text.lower())
    else:
        return word in text.lower()


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


def any_talent_match(v):
    for name, aliases in get_talents().items():
        if talent_match(name, aliases, v):
            return True

    return False
