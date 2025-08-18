import os
import requests
from bs4 import BeautifulSoup, Tag 

try:
    from dotenv import load_dotenv
    load_dotenv()
    
    CHAT_ID = os.environ['CHAT_ID']
    DEBUG_CHAT_ID = os.environ['DEBUG_CHAT_ID']
    TOKEN = os.environ['TOKEN']
except KeyError as e:
    raise ValueError(f"Environment variable {e} is not set. Please set CHAT_ID, DEBUG_CHAT_ID and TOKEN.") from e

URL = 'https://lpnu.ua/ikni/informatsiia-dlia-studentiv-ta-abituriientiv'

def on_found(title):
    pr = {
    'chat_id' : CHAT_ID,
    'text' : '@FiremanC4\n'*6 + f'{URL}\n{title}',
    }
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", params = pr)

def on_not_found():
    pr = {
    'chat_id' : DEBUG_CHAT_ID,
    'text' : f'{URL}\nНе знайдено списків нових груп ІКНІ',
    }
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", params = pr)

def on_error(e):
    pr = {
        'chat_id': CHAT_ID,
        'text': f'Помилка: {e}',
    }
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", params=pr)

if __name__ == "__main__":
    try:
        r = requests.get(URL, timeout=10)
        r.raise_for_status()  # Raise an error for HTTP errors
    except requests.RequestException as e:
        on_error(e)
        raise ValueError("Network error or invalid response") from e

    soup = BeautifulSoup(r.text, 'html.parser')

    news = soup.select_one('#block-views-block-page-last-update-block-1 > div > div > div > div > div > span')
    if not (news and isinstance(news, Tag)):
        on_error("No news found on the page")
        raise ValueError("No news found on the page")

    if '11 місяців' not in news.text.lower():
        on_found(news.text)
    else:
        on_not_found()