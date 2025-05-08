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
        except requests.exceptions.Timeout:
            print('Failed to connect, timeout has been occured')
        except requests.exceptions.HTTPError:
            print('Some error has been occured, please try again...')
        else:
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
                choice = input('Go to the next or previous page or detail info or quit? (next, previous, detail, quit): ')

                if choice.lower().strip() == 'next':
                    page += 1
                    continue
                elif choice.lower().strip() == 'previous':
                    page -= 1
                    if page <= 0:
                        page = 1
                        print('Cannot be lower than 0')
                    continue
                elif choice.lower().strip() == 'detail':
                    try:
                        post_page = int(input('Enter a page for detail post: '))
                        post_index = int(input('Please enter post number to see detail: '))
                    except ValueError:
                        print('Please type in integer, not some other type')
                        continue

                    detail_response = requests.get(url, params={'p': post_page})
                    detail_soup = BeautifulSoup(detail_response.text, 'lxml')
                    post_rank = 1
                    post_check = False

                    for post in detail_soup.find_all('tr', class_='athing submission'):

                        if post_index == post_rank:
                            tbody = detail_soup.find('table', id='hnmain').find_all('tr')[3].td.table
                            sublines = tbody.find_all('tr', class_=None)
                            try:
                                del sublines[30]
                            except IndexError:
                                pass
                            subline = sublines[post_index - 1]
                            post_title = post.find_all('td', class_='title')[1].find('span', class_='titleline').a.text
                            post_url = post.find_all('td', class_='title')[1].find('span', class_='titleline').a.get('href')
                            post_author = subline.find('td', class_='subtext').span.find('a', class_='hnuser').text
                            post_time = subline.find('td', class_='subtext').find('span', class_='age').a.text
                            print('-' * 10)
                            print(f'Title: {post_title}')
                            print(f'Url: {post_url}')
                            print(f'Author: {post_author}')
                            print(f'Created: {post_time}')
                            post_check = True
                            break
                        else:
                            post_rank += 1
                            continue
                    if not post_check:
                        print("There is nothing, maybe you typed wrong post that doesn't exist?")
                        break
                    print('-' * 10)
                    print('Restart script if you need!')
                    break
                elif choice.lower().strip() == 'quit':
                    print('Goodbye!')
                    break
                else:
                    print('Choose something one from given')
                    continue
            else:
                print(f'Error: {response.status_code}')
                break

news_parser()