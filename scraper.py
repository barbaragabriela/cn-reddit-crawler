from collections import defaultdict
import json
import requests
from bs4 import BeautifulSoup


def scrape():
    '''
    Method used to get a json of all the subreddits related to a reddit tag from http://metareddit.com
    '''
    r = requests.get(
        url='http://metareddit.com/tags/',
        headers={
            'X-Requested-With': 'XMLHttpRequest'
        }
    )

    s = BeautifulSoup(r.text)

    links = []
    subs = defaultdict(list)
    for r in s.findAll('span'):
        sources=r.findAll('a',{"href":True})
        for source in sources:
            links.append(source['href'])

    unique_links = set(links)
    links = list(unique_links)
    print len(links)

    for link in links:
        print link
        x = requests.get(
            url='http://metareddit.com{}'.format(link),
            headers={
                'X-Requested-With': 'XMLHttpRequest'
            }
        )

        y = BeautifulSoup(x.text)

        for r in y.findAll('a', {"class":"subreddit-link"}):
            # print r['href']
            subs[link].append(r['href'])

    
    # data = json.dumps(subs)
    with open('data.txt', 'w') as outfile:
        json.dump(subs, outfile)


if __name__ == '__main__':
    scrape()