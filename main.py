import os
import requests
from bs4 import BeautifulSoup, Tag 

try:
    CHAT_ID = os.environ['CHAT_ID']
    TOKEN = os.environ['TOKEN']
except KeyError as e:
    raise ValueError(f"Environment variable {e} is not set. Please set CHAT_ID and TOKEN.") from e

URL = 'https://lpnu.ua/ikni'

def on_found(title):
    pr = {
    'chat_id' : CHAT_ID,
    'text' : '@FiremanC4\n'*6 + f'{URL}\n{title}',
    }
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", params = pr)

def on_not_found():
    pr = {
    'chat_id' : CHAT_ID,
    'text' : f'{URL}\nНе знайдено списків студентів ІКНІ',
    }
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", params = pr)

if __name__ == "__main__":
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, 'html.parser')

    news = soup.find('div', class_='views-view-grid horizontal cols-3 clearfix')
    if not (news and isinstance(news, Tag)):
        raise ValueError("No news found on the page")
    titles = [t.text for t in news.find_all('h3')]

    for title in titles:
        if 'списки студентів ікні' in title.lower():
            on_found(title)
            break
    else:
        on_not_found()