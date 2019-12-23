## r-compliments
A very simple reddit bot that looks for simple compliments in comments on new posts and replies directing those 
compliments back to the poster.

## Setup
###### Note: Poetry, which is used to manage project dependencies, requires python 3.7+ 

Clone the repository:
```commandline
git clone https://github.com/brentcklein/r-compliments.git
```

install poetry
```commandline
cd r-compliments
pip install -r requirements.txt
```

install project dependencies
```commandline
poetry install
```

## Environment variables
The bot relies on five environment variables in order to connect to Reddit: `praw_client_id`, `praw_client_secret`, 
`praw_username`, `praw_password`, and `praw_user_agent`. `praw_username` and `praw_password` are the username and 
password for the Reddit account you wish to use. Follow 
[these instructions (under "Create Reddit App")](https://www.pythonforengineers.com/build-a-reddit-bot-part-1/) to 
create a Reddit app in order to obtain a `client_id` and `client_secret`, and [Reddit's guidelines for creating a 
user-agent string (under "Rules")](https://github.com/reddit-archive/reddit/wiki/API).

## Running locally 

To run the bot locally, simply call:
```commandline
python app.bot
```
Use CTRL+C to stop the bot at any time.

## Deploying to Heroku

The app is also set up to deploy to Heroku. Follow 
[Heroku's instructions to install the heroku cli](https://devcenter.heroku.com/articles/getting-started-with-python#set-up), 
[create an heroku application](https://devcenter.heroku.com/articles/getting-started-with-python#deploy-the-app), and
[set the required environment variables](https://devcenter.heroku.com/articles/config-vars). 
(Instead of `heroku ps:scale web=1`, call `heroku ps:scale worker=1` to ensure that at least one instance of the bot is
running.)

You can confirm that the bot is running by calling `heroku logs --tail`
