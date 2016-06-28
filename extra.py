import json
import itertools as it
from collections import defaultdict

import helper


def get_subreddit_list_with_user():
    '''
    Reads json dumps from reddit and gets all the subreddits a user interacted with
    '''
    subreddits = defaultdict(list)
    with open('DATA/RC_2200000') as file:
        for row in file:
            qresult = json.loads(row)
            author = qresult["author"]
            subreddit = qresult["subreddit"]
            subreddits[author].append(subreddit)

    return subreddits


def add_relationship(user_and_subreddits):
    relationships = defaultdict(list)
    labels = {}
    ID = 1
    for user in user_and_subreddits:
        for subset in it.permutations(user_and_subreddits[user], 2):
            # add labels
            if subset[0] in labels:
                continue
            else:
                labels[subset[0]] = ID
                ID += 1
            if subset[1] in labels:
                continue
            else:
                labels[subset[1]] = ID
                ID += 1

            if subset[1] in relationships:
                if subset[0] in relationships[subset[1]]:
                    continue
            else:
                if subset[1] not in relationships[subset[0]]:
                    relationships[subset[0]].append(subset[1])

    return relationships, labels
