import requests
from bs4 import BeautifulSoup
import pandas as pd


def download_image(url, file_path):
    r = requests.get(url, stream=True)

    if r.status_code == 200:
        with open(file_path, "wb") as f:
            f.write(r.content)


if __name__ == '__main__':
    page_url_base = 'https://www.arita-marukei.com/?mode=cate&cbid=2482976&csid=0'
    page_num = 52
    img_url_base = 'https://www.arita-marukei.com/'
    urls = []

    # csvからリンクの取得
    df = pd.read_csv('40_urls.csv')
    urls = list(df['URL'])

    # 取得したリンクから画像を取得
    for i, url in enumerate(urls):
        print(i)
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        contents = soup.find('ul', class_='product__gallery')
        img_elements = contents.find_all('img')
        img_urls = []
        for img_elements in img_elements:
            img_urls.append(img_elements.get('src'))
        # print(*img_urls, sep='\n')
        for i, img_url in enumerate(img_urls):
            file_name = '{}_{}.png'.format(url[url.find('=') + 1:], i)
            image_path = 'images_40/{}'.format(file_name)
            download_image(url=img_url, file_path=image_path)
