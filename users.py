import csv


def get_top_users():
    top_users = {}

    with open('DATA/top_users.csv') as file:
        reader = csv.DictReader(file)
        for row in reader:
            username = row['USERNAME']
            karma = int(row['KARMA'])
            top_users[username] = karma

    return top_users
