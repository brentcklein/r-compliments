import json

from config import Site
from praw.exceptions import APIException

site = Site()
sub = site.subreddit('all')
self_name = site.user.me().name
print(f"logged in as {self_name}")

subjects = [
    "it's",
    "it is",
    "this's",
    "this is",
    "that's",
    "that is",
    "you're",
    "you are",
    "they're",
    "they are",
    "he's",
    "he is"
]

adverbs = [
    "so",
    "super",
    "very",
    "incredibly",
    "pretty",
    "really"
]

compliments = [
    "cool",
    "neat",
    "awesome",
    "amazing",
    "fantastic",
    "perfect",
    "beautiful",
    "interesting",
    "great",
    "an inspiration"
]

with open('subreddits.json') as json_file:
    subreddits = json.load(json_file)

restricted_subreddits = subreddits['restricted']


def reply_to_comment(c, m):
    c.reply(m)


def thread_is_suitable(c):
    return \
        c.submission.subreddit.display_name not in restricted_subreddits and \
        not c.submission.subreddit.over18 and \
        'serious' not in c.submission.title.lower() and \
        c.author is not None and \
        c.author.name != self_name


# get a stream of new comments
print("monitoring new comments...")
comments_checked = 0
compliments_found = 0
replies_made = 0

for comment in sub.stream.comments(skip_existing=True):
    comments_checked += 1
    if compliments_found > 0 and compliments_found % 10 == 0 or comments_checked % 100 == 0:
        print(f"comments checked: {comments_checked}; compliments found: {compliments_found}")

    # Check for thread suitability
    if not thread_is_suitable(comment):
        continue

    compliment_used = None
    message = None

    # check each comment for any combination of objects, [adverbs], and compliments
    for subject in subjects:
        for compliment in compliments:
            if f"{subject} {compliment}" in comment.body.lower():
                compliment_used = compliment
                break
            for adverb in adverbs:
                if f"{subject} {adverb} {compliment}" in comment.body.lower():
                    compliment_used = f"{adverb} {compliment}"
                    break
            if compliment_used is not None:
                break

    if compliment_used is not None:
        # check each comment with a compliment for a response from self
        # if no response, respond
        if self_name not in [reply.author.name for reply in list(comment.replies) if reply.author is not None]:
            compliments_found += 1
            print(f"posting reply in {comment.subreddit.display_name}")
            if comment.parent().author.name == self_name:
                # We're being complimented!
                message = f"Awww, thanks u/{comment.author.name}. =)"
            elif compliment_used == 'great':
                # r/beetlejuicing incoming
                message = f"Check my username, u/{comment.author.name}. =)"
            else:
                message = f"*You're* {compliment_used}, u/{comment.author.name}!"

            try:
                reply_to_comment(comment, message)
                replies_made += 1
            except APIException as e:
                # We expect rate limit issues since the account is new and we're processing a lot of comments
                # quickly. Log those exceptions, but also raise any others.
                print(f'Encountered API exception: {str(e)}')
                if "RATELIMIT" not in str(e):
                    raise e
