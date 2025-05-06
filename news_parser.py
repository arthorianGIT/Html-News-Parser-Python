import requests
from bs4 import BeautifulSoup
import lxml

index = 1
url = 'https://news.ycombinator.com/'
page = 1

def news_parser():
    global index
    global url
    global page
    params = {
        'p': page
    }
    while True:
        try:
            response = requests.get(url, params=params)
        except requests.exceptions.ConnectionError:
            print('Failed to connect, please check your internet connection')

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            for span in soup.find_all('span', class_='titleline'):
                hyperlink_text = span.find('a').text
                hyperlink_link = span.find('a').get('href')
                print('-' * 10)
                print(f'{index} - {hyperlink_text} -> {hyperlink_link}')
                index += 1
            print('-' * 10)
            choice = input('Go to the next or previous page or quit? (next, previous, quit): ')

            if choice.lower().strip() == 'next':
                page += 1
                continue
            elif choice.lower().strip() == 'previous':
                page -= 1
                continue
            elif choice.lower().strip() == 'quit':
                print('Goodbye!')
                break
        else:
            print(f'Error: {response.status_code}')

news_parser()