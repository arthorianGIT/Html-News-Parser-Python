import requests
from bs4 import BeautifulSoup
import lxml

url = 'https://news.ycombinator.com/'
page = 1
index = 0

def news_parser():
    global url
    global index
    global page
    while True:
        params = {
        'p': page
        }
        try:
            response = requests.get(url, params=params)
        except requests.exceptions.ConnectionError:
            print('Failed to connect, please check your internet connection')

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            for span in soup.find_all('span', class_='titleline'):
                hyperlink_text = span.find('a').text
                hyperlink_link = span.find('a').get('href')
                for rank in soup.find_all('span', class_='rank'):
                    index = rank.text
                    del rank['class']
                    break
                print('-' * 10)
                print(f'{index} {hyperlink_text} -> {hyperlink_link}')
            print('-' * 10)
            choice = input('Go to the next or previous page or quit? (next, previous, quit): ')

            if choice.lower().strip() == 'next':
                page += 1
                continue
            elif choice.lower().strip() == 'previous':
                page -= 1
                if page <= 0:
                    page = 1
                    print('Cannot be lower than 0')
                continue
            elif choice.lower().strip() == 'quit':
                print('Goodbye!')
                break
            else:
                print('Choose something one from given')
                continue
        else:
            print(f'Error: {response.status_code}')

news_parser()