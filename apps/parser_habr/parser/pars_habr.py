import json
import logging
import requests
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from aiohttp_retry import RetryClient, ExponentialRetry
from apps.parser_habr.models import Task
from .database import Database
from .config import settings


class ParserHub:

    hub_dict: dict = {}
    articles: list = []

    def __init__(self):
        self.db = Database()
        self.logger = logging.getLogger('main')
        self.head = settings.get_headers()

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
                    print('get_info_article', author)
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

    async def collect_info_articles(self, lst_links: list[str], hub_name: str, hub_link: str, headers: dict) -> None:
        """"Input: a list of link to a hub. Output: json with hub-name, hub-link and all articles"""""

        self.logger.info(f'Fn {self.collect_info_articles.__name__} has started')

        try:
            self.hub_dict['Hub_name'] = hub_name
            self.hub_dict['Hub_link'] = hub_link
            self.hub_dict['Hub_articles'] = self.articles

            async with aiohttp.ClientSession(headers=headers) as session:
                tasks = []
                for link in lst_links:
                    task = asyncio.create_task(self.get_info_article(session=session, link_article=link, headers=headers))
                    tasks.append(task)
                await asyncio.gather(*tasks)

            self.logger.info(f'Fn {self.collect_info_articles.__name__}. Info articles was collected successfully')

        except Exception as ex:
            self.logger.info(f'Fn {self.collect_info_articles.__name__}. Failed to collect info from articles of a hub. Message: {ex}')

    def __call__(self, celery_task_id, list_hubs: str) -> None:
        new_task = Task.objects.create(celery_task_id=celery_task_id)
        for hub_item in list(list_hubs):
            name = hub_item['hub_name']
            link = hub_item['hub_link']

            # we collect all articles from a hub and put them in json
            links_pages = self.get_links_article(url_hub=link, headers=self.head)
            asyncio.run(self.collect_info_articles(lst_links=links_pages, hub_name=name, hub_link=link, headers=self.head))

            #print(self.hub_dict)
            # insert into db
            self.db.insert_authors(self.hub_dict)
            self.db.insert_articles(self.hub_dict)
        new_task.is_success = True
        new_task.save()
