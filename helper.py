import wrapper
import itertools as it


def get_history(username):
    '''
    Get a list of subreddits where a user has commented and sumbitted posts
    '''
    commented_subs = wrapper.get_subreddits_by_user_comment(username)
    submitted_subs = wrapper.get_subreddits_by_user_submission(username)

    combined = list(commented_subs)
    combined.extend(submitted_subs)

    unique_subreddits = set(combined)
    unique_subreddits = list(unique_subreddits)

    return unique_subreddits


def add_relationship(relationships, subreddit_list):
    '''
    Get the relationships between subreddits made by the user
    '''
    for subset in it.permutations(subreddit_list, 2):
        if subset[1] in relationships:
            if subset[0] in relationships[subset[1]]:
                continue
        else:
            if subset[1] not in relationships[subset[0]]:
                relationships[subset[0]].append(subset[1])

    # print relationships
    return relationships


def get_subreddit_list(username):
    subreddits = []
    print username
    with open('DATA/users/sub_' + username + '.txt') as file:
        for row in file:
            subreddits.append(row.rstrip())

    return subreddits


def collect_data():
    '''
    Gets all the subreddit list the users interact with
    This function is only used for collecting data purposes (just once)
    '''
    # Get users
    top_users = users.get_top_users()

    for username in top_users:
        subreddits = get_history(username)
        save_to_file(username, subreddits)


def save_to_file(username, subreddit_list):
    '''
    Writes to file all the subreddits a user interacts with
    '''
    file = open('DATA/sub_{}.txt'.format(username), 'w')
    for subreddit in subreddit_list:
        file.write(subreddit + '\n')
    file.close()


def add_labels(labels, relationships, ID):
    '''
    Create labels for nodes so pajek works
    '''
    for node in relationships:
        if node in labels:
            continue
        labels[node] = ID
        ID += 1

    return ID


def write_pajek(labels, relationships):
    '''
    Writes all relationships to a pajek file
    '''
    file = open('pajek/top_users.net', 'w')
    file.write('*Vertices ')
    file.write(str(len(labels)))
    file.write('\n')
    for label in labels:
        file.write(str(labels[label]) + ' ' + label + '\n')
    file.write('*Edges')
    file.write('\n')
    for node in relationships:
        for connection in relationships[node]:
            file.write(str(labels[node]) + ' ' + str(labels[connection]) + '\n')

    file.close()