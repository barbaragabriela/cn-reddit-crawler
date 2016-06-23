import praw
import OAuth2Util


LIMIT = 10

r = praw.Reddit("Useragent")
o = OAuth2Util.OAuth2Util(r)


def get_subreddits_by_user_comment(username):
    '''
    returns a list of unique subreddit names where the user commented
    '''
    user = r.get_redditor(username)
    comments = user.get_comments(limit=LIMIT)

    subreddits = []
    for comment in comments:
        try:
            subreddit = comment.subreddit.display_name
            subreddits.append(subreddit)
        except praw.errors.NotFound:
            print "ERROR: {} not found".format(username)
            continue

    unique_subreddits = set(subreddits)
    unique_subreddits = list(unique_subreddits)

    return unique_subreddits


def get_subreddits_by_user_submission(username):
    '''
    returns a list of unique subreddit names where the user submitted a post
    '''
    user = r.get_redditor(username)
    submissions = user.get_submitted(limit=LIMIT)

    subreddits = []
    for submission in submissions:
        try:
            subreddit = submission.subreddit.display_name
            subreddits.append(subreddit)
        except praw.errors.NotFound:
            print "ERROR: {} not found".format(username)
            continue

    unique_subreddits = set(subreddits)
    unique_subreddits = list(unique_subreddits)

    return unique_subreddits