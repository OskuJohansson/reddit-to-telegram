import database as db
from os import environ
from datetime import datetime, timedelta


def cleanup():
    print('Starting cleanup job')
    current_time = datetime.now()
    buffer_ttl = int(environ["buffer_ttl"])
    buffer_age_limit = current_time - timedelta(days=buffer_ttl)

    buffer = db.get_buffer()
    updated_buffer = []
    for post in buffer:
        post_date = datetime.utcfromtimestamp(post["date"])
        if post_date > buffer_age_limit:
            updated_buffer.append(post)
        else:
            print(f'Post {post["id"]} was posted on {post_date}, it will be removed from buffer')

    db.update_buffer(updated_buffer)


def lambda_handler(event=None, context=None):
    cleanup()
