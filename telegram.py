from os import environ

import requests


def send_message(post):
    token = environ["telegram_bot_token"]
    chat_handle = environ["telegram_chat_id"]
    text = __form_text(post)
    body = {
        'chat_id': chat_handle,
        'text': text,
        'parse_mode': 'HTML',
        'disable_web_page_preview': True
    }
    print(body)
    response = requests.post(f'https://api.telegram.org/bot{token}/sendMessage', data=body)
    if response.status_code == 200:
        print(f'Response from sending message to Telegram: {response.text}')
    else:
        raise requests.exceptions.BaseHTTPError(f'Error sending message to Telegram: {response.text}')


def __form_text(post):
    title = str(post.title).replace('<', '&lt;').replace('>', '&gt;').replace('&', '&amp;').replace('\"', '&quot;')
    link = post.permalink
    return f'{title} [<a href="www.reddit.com{link}">Reddit thread</a>]'
