import users
import helper

from collections import defaultdict
import data_collector as dc

def main():
    relationships = defaultdict(list)
    labels = {}
    last_label_id = 1

    # Get users
    top_users = users.get_top_users()

    # Loop through users and get the list of subreddits they comment and post
    for username in top_users:
        subreddits = helper.get_subreddit_list(username)
        helper.add_relationship(relationships, subreddits)
        last_label_id = helper.add_labels(labels, subreddits, last_label_id)

    helper.write_pajek(labels, relationships)


if __name__ == '__main__':
    main()