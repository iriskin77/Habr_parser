import logging
import aiohttp
import asyncio
import requests
from aiohttp_retry import RetryClient, ExponentialRetry
from bs4 import BeautifulSoup
from apps.parser_mel.models import Task
from apps.parser_mel.parser.database import Database
from apps.parser_mel.parser.config import settings


class ParserMel:

    mel_dict: dict = {}

    main: str = "https://mel.fm"

    def __init__(self):
        self.db = Database()
        self.logger = logging.getLogger('main')
        self.head = settings.get_headers()


    def get_articles(self, main_url: str, head: dict) -> list[str]:
        self.logger.info(f'Fn get_articles has started')
        try:
            resp = requests.get(url=main_url, headers=head)
            soup = BeautifulSoup(resp.text, "lxml")
            links = soup.find_all('a', class_="b-pb-article-card__link")
            links_articles = [self.main + link["href"] for link in links]
            self.logger.critical(f'Fn get_articles has finished correctly')
            return links_articles
        except:
            self.logger.critical(f'Fn get_articles has finished incorrectly')

    async def collect_info_article(self, session, link: str, head: dict) -> None:

        retry_options = ExponentialRetry(attempts=5)
        retry_client = RetryClient(raise_for_status=False, retry_options=retry_options, client_session=session, start_timeout=0.5)

        try:
            async with retry_client.get(url=link, headers=head) as response:

                if response.ok:

                    resp = await response.text()
                    soup = BeautifulSoup(resp, "lxml")

                    title = soup.find('h1', class_="b-pb-article__title b-pb-article__title_with-cover").get_text(strip=True)
                    body = soup.find('div', class_="b-pb-publication-body b-pb-publication-body_pablo").get_text(strip=True)
                    date = soup.find('div', class_="publication-header__publication-date").get_text(strip=True)

                    self.mel_dict["Mel_articles"].append({
                        'title': title,
                        'body': body,
                        'link_article': link,
                        'date_published': date,
                    })
        except:
            self.logger.warning(f'Fn collect_info_article. Failed to collect article data')

    async def collect_info_articles(self, links: list[str], head: dict, mel_cat: str, mel_cat_link: str) -> None:
        self.logger.info(f'Fn collect_info_articles has started')

        try:
            self.mel_dict["Mel_cat"] = mel_cat
            self.mel_dict["Mel_cat_link"] = mel_cat_link
            self.mel_dict["Mel_articles"] = []

            async with aiohttp.ClientSession(headers=head) as session:
                tasks = []
                for link in links:
                    task = asyncio.create_task(self.collect_info_article(session=session, link=link, head=head))
                    tasks.append(task)
                await asyncio.gather(*tasks)
            self.logger.info(f'Fn collect_info_articles has finished correctly')
        except:
            self.logger.critical(f'Fn collect_info_articles has finished incorrectly')

    def __call__(self, celery_task_id: str, list_cat: str) -> None:
        self.logger.info(f'Parser_mel has started')
        try:
            new_task = Task.objects.create(celery_task_id=celery_task_id)
            for item in list(list_cat):
                name = item['name_cat']
                link_cat = item['link_cat']

                links = self.get_articles(main_url=link_cat, head=self.head)
                asyncio.run(self.collect_info_articles(links, self.head, name, link_cat))
                self.db.insert_articles(self.mel_dict)

            new_task.is_success = True
            new_task.save()
        except:
            self.logger.info(f'Parser_mel has finished correctly')
