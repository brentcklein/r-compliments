import os
from praw import Reddit as Site

client_id = os.environ['praw_client_id']
client_secret = os.environ['praw_client_secret']
username = os.environ['praw_username']
password = os.environ['praw_password']
user_agent = os.environ['praw_user_agent']

