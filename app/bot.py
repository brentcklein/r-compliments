import praw
from config import Site

site = Site()
sub = site.subreddit('qicksilvershangout')

# run every thirty minutes
# get most recent submissions
for submission in sub.new(limit=None):
    # get all comments from each submission
    for comment in submission.comments.list():
        have_replied = False
        # check each comment for required substring
        if "testing self" in comment.body.lower():
            # check each matching comment for a response from self
            for reply in list(comment.replies):
                if reply.author.name == 'no_ur_great':
                    have_replied = True
            # if no response, respond
            if not have_replied:
                comment.reply(f"Test complete, u/{comment.author.name}!")


