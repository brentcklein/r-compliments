import time

from config import Site

site = Site()
sub = site.subreddit('qicksilvershangout+gonewild')

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
    "pretty"
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
    "incredible",
    "an inspiration"
]

while True:
    # get most recent submissions
    for submission in sub.new(limit=None):
        # Avoid the rough side of town
        if submission.subreddit.over18:
            continue

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
                        break

                if compliment_used is None:  # Don't bother checking adverbs if we already have a compliment
                    for adverb in adverbs:
                        for compliment in compliments:
                            if f"{subject} {adverb} {compliment}" in comment.body.lower():
                                is_compliment = True
                                compliment_used = f"{adverb} {compliment}"
                                break

            if is_compliment:
                # check each matching comment for a response from self
                if 'no_ur_great' not in [reply.author.name for reply in list(comment.replies)]:
                    should_reply = True
                # if no response, respond
                if should_reply:
                    if comment.parent().author.name == 'no_ur_great':
                        # We're being complimented!
                        comment.reply(f"Awww, thanks u/{comment.author.name}. =)\n\nu/therealqicksilver hopes you're "
                                      f"having a great day!")
                    elif compliment_used == 'great':
                        # r/beetlejuicing incoming
                        comment.reply(f"Check my username, u/{comment.author.name}. =)")
                    else:
                        comment.reply(f"*You're* {compliment_used}, u/{comment.author.name}!")

    # run every thirty minutes
    time.sleep(30)
