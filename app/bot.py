import time

from config import Site

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

print("monitoring new comments...")
while True:
    # get a stream of new comments
    comments_checked = 0
    compliments_found = 0
    for comment in sub.stream.comments(skip_existing=True):
        comments_checked += 1
        if compliments_found > 0 and compliments_found % 10 == 0 or comments_checked % 100 == 0:
            print(f"comments checked: {comments_checked}; compliments found: {compliments_found}")
        # Avoid the rough side of town
        if comment.subreddit.over18:
            continue

        if comment.author is None or comment.author.name == self_name:
            # Don't compliment self, would get caught in a loop, as well as being tacky
            # Skip comments without an author
            continue

        compliment_used = None

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
                    comment.reply(f"Awww, thanks u/{comment.author.name}. =)")
                elif compliment_used == 'great':
                    # r/beetlejuicing incoming
                    comment.reply(f"Check my username, u/{comment.author.name}. =)")
                else:
                    comment.reply(f"*You're* {compliment_used}, u/{comment.author.name}!")

    # Refresh the stream every fifteen minutes if no new comments are yielded
    print("sleeping...")
    time.sleep(900)
