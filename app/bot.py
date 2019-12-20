import time

from config import Site

site = Site()
sub = site.subreddit('qicksilvershangout')

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

compliments = [
    "cool",
    "neat",
    "awesome",
    "amazing",
    "fantastic",
    "perfect",
    "beautiful",
    "interesting",
    "great",  # TODO: if compliment is "great," tell commenter to check username
    "incredible",
    "an inspiration"
]

while True:
    # get most recent submissions
    for submission in sub.new(limit=None):
        # get all comments from each submission
        for comment in submission.comments.list():
            if comment.author.name == 'no_ur_great':
                # Don't compliment self, would get caught in a loop
                continue

            is_compliment = False
            should_reply = False
            compliment_used = None

            # check each comment for any combination of objects and compliments
            for subject in subjects:
                for compliment in compliments:
                    if f"{subject} {compliment}" in comment.body.lower():
                        is_compliment = True
                        compliment_used = compliment

            if is_compliment:
                # check each matching comment for a response from self
                if 'no_ur_great' not in [reply.author.name for reply in list(comment.replies)]:
                    should_reply = True
                # if no response, respond
                if should_reply:
                    comment.reply(f"*You're* {compliment_used}, u/{comment.author.name}!")

    # run every thirty minutes
    time.sleep(30)
