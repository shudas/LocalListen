import re
import sys
import os.path

import requests
from bs4 import BeautifulSoup

from config.config_parser import get_config


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from models.db_helper import create_table, insert_values

# these are from the discogs webpage: http://www.discogs.com/help/submission-guidelines-release-genres-styles.html
separate_genres = [
    "blues",
    "brass",
    "military",
    "children's",
    "classical",
    "electronic",
    "folk",
    "world",
    "country",
    "funk",
    "soul",
    "hip-hop",
    "jazz",
    "latin",
    "non-music",
    "pop",
    "reggae",
    "rock",
    "stage & screen"
]
genre_url = "http://reference.discogslabs.com/browse/style"
page_param = 'page'


def get_style_from_page(page_id=1):
    ret = set()
    params = {'page': page_id}
    r = requests.get(genre_url, params=params)
    if r.status_code == requests.codes.ok:
        soup = BeautifulSoup(r.content)
        all_style_links = soup.find_all(href=re.compile('style/*'))
        for tag in all_style_links:
            ret.add(tag.string.lower())
    return ret


# currently there are 17 pages on discogs
def get_n_pages(n=17):
    ret = set()
    for i in range(n):
        ret = ret | get_style_from_page(i + 1)
    return ret


def get_all_genres():
    return set(separate_genres) | get_n_pages()


def get_and_store():
    genres = get_all_genres()
    # first try to create the genre table. should not create if exists
    ddl = 'genre VARCHAR(50) PRIMARY KEY'
    create_table(get_config()['Tables']['genre'], ddl)
    for genre in genres:
        insert_values(get_config()['Tables']['genre'], 'genre', genre)

if __name__ == '__main__':
    get_and_store()
