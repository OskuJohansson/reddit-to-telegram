from os import environ

import praw
import praw.models

import database as db
import telegram as tg


def setup_reddit():
    reddit = praw.Reddit(client_id=environ["reddit_client_id"],
                         client_secret=environ["reddit_client_secret"],
                         user_agent=environ["reddit_user_agent"])
    return reddit


def get_posts():
    reddit = setup_reddit()
    subreddit_name = environ["reddit_subreddit"]
    print('Getting Top Posts From r/' + subreddit_name)
    return reddit.subreddit(subreddit_name).top(limit=100, time_filter='day')


def to_buffer_format(post):
    new_post = dict()
    new_post["id"] = post.id
    new_post["date"] = int(post.created_utc)
    return new_post


def app():
    top_posts = get_posts()
    buffer = db.get_buffer()
    buffer_ids = [d['id'] for d in buffer]
    print(f'Buffer ID\'s: {buffer_ids}. Length {len(buffer_ids)}')
    new_posts = []
    score = int(environ["reddit_score"])

    for post in top_posts:
        if post.score >= score and post.id not in buffer_ids:
            print(f'The post {post.id} is valid for publishing ({post.score} upvotes, {score} needed)')
            tg.send_message(post)
            new_posts.append(to_buffer_format(post))
            db.put_to_archive(post)

    if len(new_posts) > 0:
        db.put_in_buffer(new_posts)


def lambda_handler(event=None, context=None):
    app()
