import requests
from bs4 import BeautifulSoup
import csv

CSV = 'alta.csv'
HOST = "https://alta.ge/"
URL = "https://alta.ge/phones-and-communications/smartphones.html"
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
}

# sruli htmls amogeba 200


def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all(
        'div', class_='ty-column3')
    cards = []
    for item in items:
        cards.append(
            {
                'title': item.find('a', class_='product-title').get_text(),
                'price': item.find('span', class_='ty-price-num').get_text(),
                'link': item.find('div', class_='ty-grid-list__item-name').find('a').get('href'),
            }
        )
    return cards

# shenaxva


def save_doc(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['sataurebi', 'fasebi', 'linkebi'])
        for item in items:
            writer.writerow([item['title'], item['price'], item['link']])


# globaluri parsi gverdebistvis
def parser():
    PAGENATION = input('How much page you want parse ? :')
    PAGENATION = int(PAGENATION.strip())
    html = get_html(URL)
    if html.status_code == 200:
        cards = []
        for page in range(1, PAGENATION):
            print(f'Parsing page is : {page}')
            html = get_html(URL, params={'page': page})
            cards.extend(get_content(html.text))
            save_doc(cards, CSV)
        pass
    else:
        print('Error')


parser()
