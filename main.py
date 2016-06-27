import users
import helper

from collections import defaultdict
import data_collector as dc

def main():
    option = ''
    while option != '0':
        print 'What do you want to do?'
        print '1) Get data from top users.'
        print '2) Generate pajek files'
        print '3) Smooth the trigram language model'
        print '0) Exit'
        print 'Choice: '
        option = raw_input()

        if option == '1':
            helper.collect_data()
        elif option == '2':
            relationships = defaultdict(list)
            comments_relationships = defaultdict(list)
            posts_relationships = defaultdict(list)

            labels = {}
            comments_labels = {}
            posts_labels = {}

            last_label_id = 1
            c_last_label_id = 1
            p_last_label_id = 1
            # Get users
            # top_users = users.get_top_users()
            top_users = ['barbss', 'metalan', 'fadeblack13']

            # Loop through users and get the list of subreddits they comment and post
            for username in top_users:
                # Create the network
                print username
                # subreddits = helper.get_subreddit_list(username)
                subreddits, commented_subs, posts_subs = helper.get_subreddit_list(username)

                # Combination of comments and posts
                relationships = helper.add_relationship(relationships, subreddits)
                last_label_id = helper.add_labels(labels, subreddits, last_label_id)
                helper.write_pajek(labels, relationships, 'top_users')
                helper.write_json(labels, relationships, 'top_users')
                # Comments
                comments_relationships = helper.add_relationship(comments_relationships, commented_subs)
                c_last_label_id = helper.add_labels(comments_labels, commented_subs, c_last_label_id)

                # Posts
                posts_relationships = helper.add_relationship(posts_relationships, posts_subs)
                p_last_label_id = helper.add_labels(posts_labels, posts_subs, p_last_label_id)

            # Testing
            # helper.write_pajek(labels, relationships, 'test_users')
            # helper.write_json(labels, relationships, 'test_users')

            helper.write_pajek(labels, relationships, 'top_users')
            helper.write_json(labels, relationships, 'top_users')

            helper.write_pajek(comments_labels, comments_relationships, 'users_comments')
            helper.write_json(comments_labels, comments_relationships, 'users_comments')

            helper.write_pajek(posts_labels, posts_relationships, 'users_posts')
            helper.write_json(comments_labels, comments_relationships, 'users_comments')

    # helper.get_subreddit_list_with_user()


if __name__ == '__main__':
    main()