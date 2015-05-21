import requests, sys, re, codecs
from bs4 import BeautifulSoup


genre_url = "http://reference.discogslabs.com/browse/style"
page_param = 'page'


def get_style_from_page(page_id=1, f=None):
    print('running scraper with param ', page_id)
    params = {'page': page_id}
    r = requests.get(genre_url, params=params)
    if r.status_code == requests.codes.ok:
        soup = BeautifulSoup(r.content)
        all_style_links = soup.find_all(href=re.compile('style/*'))
        for tag in all_style_links:
            print tag.string
            # this means write to the file object
            if f:
                try:
                    f.write(tag.string + '\n')
                    print 'writing succeeded'
                except:
                    print 'writing failed'


# currently there are 17 pages
def get_n_pages(n=17):
    f = codecs.open('genres', 'w', encoding='utf8')
    for i in range(n):
        get_style_from_page(i + 1, f)
    f.close()

if __name__ == '__main__':
    get_n_pages(int(sys.argv[1]))
