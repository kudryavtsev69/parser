import requests
from bs4 import BeautifulSoup
import csv

URL = "https://ria.ru/world/"  # Адресс сайта новостей
HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 '
                         'YaBrowser/21.9.1.600 (beta) Yowser/2.5 Safari/537.36',
           'accept': '*/*'}

FILE = 'news.txt'

def get_html(url, params=None): # Запрос
    r = requests.get(url, headers=HEADERS, params=params)
    return  r

def get_content(html): # Получение контента
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='list-item__content')

    news = []
    for item in items:
        news.append({
            'title': item.find('a', class_='list-item__title color-font-hover-only').get_text(strip=True),
            # Получаем главные новости.
            'link': item.find('a', class_='list-item__title color-font-hover-only').get('href'), # получаем ссылку на
            # новости.
            #'time': item.find('div', class_='list-item__date').get_text()
        })
    return news

def save_file(items, path): # Сохраняем новости в электронной таблице
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Тема', 'Ссылка'])
        for item in items:
            writer.writerow([item['title'], item['link']])

def parse():  #  Парсинг сайта новостей
    html = get_html(URL)
    if html.status_code == 200:

        print(get_content(html.text))
        news = get_content(html.text)

        save_file(news, FILE)
    else:
        print('Error')

parse()