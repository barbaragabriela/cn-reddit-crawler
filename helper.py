import wrapper
import users

import json
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

    return unique_subreddits, commented_subs, submitted_subs


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

    return relationships


def get_subreddit_list(username):
    '''
    Returns the lists of subreddits combined and classified by comments or posts
    '''
    subreddits = []
    commented_subs = []
    submitted_subs = []

    with open('DATA/users/combined/sub_' + username + '.txt') as file:
        for row in file:
            subreddits.append(row.rstrip())

    with open('DATA/users/comments/sub_' + username + '.txt') as file:
        for row in file:
            commented_subs.append(row.rstrip())

    with open('DATA/users/posts/sub_' + username + '.txt') as file:
        for row in file:
            submitted_subs.append(row.rstrip())

    return subreddits, commented_subs, submitted_subs


def node_degree(relationships, labels):
    '''
    Function that returns the degrees of a graph and the average degree
    '''
    degrees = [0] * len(labels)
    average = 0
    for node in relationships:
        number_of_nodes = len(relationships[node])
        average += number_of_nodes
        degrees[labels[node] - 1] = number_of_nodes
    average = average/len(labels)
    return degrees, average


def collect_data():
    '''
    Gets all the subreddit list the users interact with
    This function is only used for collecting data purposes (just once)
    '''
    # Get users
    top_users = users.get_top_users()

    for username in top_users:
        subreddits, commented_subs, submitted_subs = get_history(username)
        save_to_file(username, subreddits, 'combined')
        save_to_file(username, commented_subs, 'comments')
        save_to_file(username, submitted_subs, 'posts')


def save_to_file(username, subreddit_list, list_type):
    '''
    Writes to file all the subreddits a user interacts with
    '''
    file = open('DATA/users/{}/sub_{}.txt'.format(list_type, username), 'w')
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


def write_pajek(labels, relationships, filename):
    '''
    Writes all relationships to a pajek file
    '''
    file = open('pajek/{}.net'.format(filename), 'w')
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


def write_json(labels, relationships, filename):
    '''
    Writes all relationships to json file used by sigma.js
    '''
    degrees, average = node_degree(relationships, labels)
    print "degrees"
    print degrees
    print "average:", average

    nodes = []
    for label in labels:
        node = {}
        node['id'] = 'n{}'.format(labels[label] - 1)
        node['label'] = label
        node['x'] = random.random()
        node['y'] = random.random()
        node['size'] = degrees[labels[label] - 1]
        print node
        break
        # nodes.append(node)

    edges = []
    i = 0
    for node in relationships:
        for connection in relationships[node]:
            edge = {}
            edge['id'] = 'n{}'.format(i)
            edge['source'] = str(labels[node] - 1)
            edge['target'] = str(labels[connection] - 1)
            i += 1
            print edge
            break
            # edges.append(edge)
        break

    # data = {}
    # data['nodes'] = nodes
    # data['edges'] = edges
    # json_data = json.dumps(data)
    # with open('json/{}.json'.format(filename), 'w') as outfile:
    #     json.dump(data, outfile)
