from bs4 import BeautifulSoup
import requests
import aiohttp
import asyncio
from fake_useragent import UserAgent
from aiohttp_retry import RetryClient, ExponentialRetry
from .models import Texts, Author, Hub
import logging

headers = {
        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Cookie': 'news_lang=ru; yandex_login=talcore; ys=udn.cDrQktC70LDQtNC40YHQu9Cw0LIg0JrQsNGA0L/QtdC90LrQvg%3D%3D#c_chck.3181849896; yandexuid=7355079031598165761; mda2_beacon=1672991591886; gdpr=0; _ym_uid=1668166334590200044; addruid=J16Al8s1i5J74M9S9pL5k1W1f9; Session_id=3:1684046607.5.0.1672991591876:1DI8uQ:15a.1.2:1|552541704.0.2|64:10009557.333765.bRabFjTPl-KB0YFwm7thxr4P1Eg; sessionid2=3:1684046607.5.0.1672991591876:1DI8uQ:15a.1.2:1|552541704.0.2|64:10009557.333765.fakesign0000000000000000000; tmr_lvid=25aa36deb66ec3f5fd31de74352c56df; tmr_lvidTS=1665515375244; _ym_d=1693207925; Zen-User-Data={%22zen-theme%22:%22light%22}; zen_sso_checked=1; rec-tech=true; _ym_isad=1; KIykI=1; crookie=GwkL3T35JZAFN7/LgkLy5B06+N//nBiHRavbYemTc3SQ283H5odlLAaFAbEviWDO04s3S8SNGtCpq/kPhcdHkItBFYI=; cmtchd=MTY5NjMwODI2NzIwOQ==; _yasc=NEEDPcWQa1OaQo640rfL6v+8e9D3HVcXi8nYWOEebBJActfjCMY2F5mAmVGLC8g6; bltsr=1; tmr_detect=1%7C1696312690921',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    }


class ParserHub:

    hub_dict: dict = {}
    articles: list = []

    def __init__(self):
        self.db = Database()
        self.logger = logging.getLogger('main')
        self.ua = UserAgent()

    def get_links_article(self, url_hub: str, headers: dict) -> list[str] | int:
        """"Input: a link to a habr-hub. Output: a list of links from the main page of a hub"""""

        self.logger.info(f'Fn {self.get_links_article.__name__} has started')

        try:
            lst_links = []

            response = requests.get(url=url_hub, headers=headers)
            soup = BeautifulSoup(response.text, "lxml")
            lst = soup.find_all("h2", class_="tm-title tm-title_h2")

            for elem in lst:
                link = "https://habr.com" + elem.find('a', class_="tm-title__link")["href"]
                lst_links.append(link)

            self.logger.info(f'Fn {self.get_links_article.__name__} Links to article were collected successfully')
            return lst_links
        except Exception as ex:
            self.logger.critical(f'Fn {self.get_links_article.__name__}. Failed to collect links to article from a hub. Message:{ex} ')

    async def get_info_article(self, session, link_article: str, headers: dict):
        """"Input: a link to am article. Output: info (author, text etc.) collected into a dict"""""

        retry_options = ExponentialRetry(attempts=5)
        retry_client = RetryClient(raise_for_status=False, retry_options=retry_options, client_session=session, start_timeout=0.5)

        try:
            async with retry_client.get(url=link_article, headers=headers) as response:

                if response.ok:

                    resp = await response.text()
                    soup = BeautifulSoup(resp, "lxml")

                    author = soup.find('a', class_="tm-user-info__username").get_text(strip=True)
                    author_link = "https://habr.com" + soup.find('a', class_="tm-user-info__username")["href"]
                    title = soup.find('h1', class_="tm-title tm-title_h1").get_text(strip=True)
                    text = soup.find('div', class_="tm-article-body").text
                    date = soup.find('span', class_="tm-article-datetime-published").find("time")["title"]

                    self.hub_dict['Hub_articles'].append({
                        'author': author,
                        'author_link': author_link,
                        'title': title,
                        'text': text,
                        'link_article': link_article,
                        'date': date,
                    })
        except Exception as ex:
            self.logger.warning(f'Fn {self.get_info_article.__name__} Failed to collect info of article. Message: {ex}')

    async def collect_info_articles(self, lst_links: list[str], hub_name: str, hub_link: str) -> None:
        """"Input: a list of link to a hub. Output: json with hub-name, hub-link and all articles"""""

        self.logger.info(f'Fn {self.collect_info_articles.__name__} has started')

        #ua = UserAgent()
        fake_ua = {'user-agent': self.ua.random}

        try:
            self.hub_dict['Hub_name'] = hub_name
            self.hub_dict['Hub_link'] = hub_link
            self.hub_dict['Hub_articles'] = self.articles

            async with aiohttp.ClientSession(headers=fake_ua) as session:
                tasks = []
                for link in lst_links:
                    task = asyncio.create_task(self.get_info_article(session=session, link_article=link, headers=fake_ua))
                    tasks.append(task)
                await asyncio.gather(*tasks)

            self.logger.info(f'Fn {self.collect_info_articles.__name__}. Info articles was collected successfully')

        except Exception as ex:
            self.logger.info(f'Fn {self.collect_info_articles.__name__}. Failed to collect info from articles of a hub. Message: {ex}')

    def __call__(self, list_hubs: str) -> None:
        for hub_item in list(list_hubs):
            name = hub_item['hub_name']
            link = hub_item['hub_link']

            # we collect all articles from a hub and put them in json
            links_pages = self.get_links_article(url_hub=link, headers=headers)
            asyncio.run(self.collect_info_articles(lst_links=links_pages, hub_name=name, hub_link=link))
            # insert into db
            self.db.insert_authors(self.hub_dict)
            self.db.insert_articles(self.hub_dict)


class Database:

    def __init__(self):
        self.logger = logging.getLogger('main')

    def insert_authors(self, json_articles: dict) -> None:
        """"Input: json with all articles from a hub. Output: the function inserts author-name and author-link in db"""""

        self.logger.info(f'Fn {self.insert_authors.__name__} has started')

        try:
            for article in json_articles['Hub_articles']:
                author_check = Author.objects.filter(author=article['author']).exists()
                if author_check == False:
                    Author.objects.create(author=article['author'], author_link=article['author_link']).save()

            self.logger.info(f'Fn {self.insert_authors.__name__}. Authors were inserted successfully')
        except Exception as ex:
            self.logger.critical(f'Fn {self.insert_authors.__name__}. Failed to insert authors. Message: {ex}')

    def insert_articles(self, json_articles: dict) -> None:

        """"Input: json with all articles from a hub. Output: the function inserts articles in db"""""

        try:
            for article in json_articles['Hub_articles']:

                hub_name = Hub.objects.filter(hub_name=json_articles['Hub_name']).first()
                author = Author.objects.filter(author=article['author']).first()

                text_check = Texts.objects.filter(title=article['title']).exists()

                if text_check == False:

                    new_text = Texts.objects.create(
                                         hub=hub_name,
                                         author=author,
                                         title=article['title'],
                                         text=article['text'],
                                         date=article['date'],
                                         link=article['link_article']
                    )
                    new_text.save()
            self.logger.info(f'Fn {self.insert_authors.__name__}. Articles were inserted successfully')
        except Exception as ex:
            self.logger.critical(f'Fn {self.insert_articles.__name__}. Failed to insert articles. Message: {ex}')
