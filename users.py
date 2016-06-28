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


def get_top_users_with_metrics():
    top_users = get_top_users()

    with open('DATA/users_comments_and_posts.csv') as file:
        reader = csv.DictReader(file)

        file = open('DATA/table.html', 'w')
        file.write("<table id=\"table\">\n")
        file.write("<tr>")
        file.write("<td><b><a target=\"_blank\" href=\"http://www.karmawhores.net/\">Top Users</a></b></td>")
        file.write("<td><b>Karma</b></td>")
        file.write("<td><b>Comments</b></td>")
        file.write("<td><b>Posts</b></td>")
        file.write("</tr>")
        for row in reader:
            username = row['USERNAME']
            comments = row['COMMENTS']
            posts = row['POSTS']
            karma = top_users[username]
            file.write("<tr>")
            file.write("<td><a target=\"_blank\" href=\"http://www.reddit.com/u/{}/\">{}</a></td>".format(username, username))
            file.write("<td>{}</td>".format(karma))
            file.write("<td>{}</td>".format(comments))
            file.write("<td>{}</td>".format(posts))
            file.write("</tr>")
        file.write("</table>\n")
        file.close