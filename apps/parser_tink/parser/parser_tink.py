import requests
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from aiohttp_retry import RetryClient, ExponentialRetry
from apps.parser_tink.models import Task
from apps.parser_tink.parser.database import Database
from apps.parser_tink.parser.config import settings


class Parser:

    main_link = "https://journal.tinkoff.ru"

    tink_dict: dict = {}
    cat_articles: list = []
    db = Database()
    head = settings.get_headers()

    def get_links_articles(self, main_url: str, headers: dict) -> list[str]:
        dct = {}
        resp = requests.get(url=main_url, headers=headers)
        soup = BeautifulSoup(resp.text, "lxml")
        res = soup.find_all('a', class_='link--OD_Qn')
        link_articles = [self.main_link + i['href'] for i in res]
        return link_articles

    async def collect_info_article(self, session, link: str, headers: dict) -> None:

        retry_options = ExponentialRetry(attempts=5)
        retry_client = RetryClient(raise_for_status=False, retry_options=retry_options, client_session=session, start_timeout=0.5)

        async with retry_client.get(url=link, headers=headers) as response:

            if response.ok:
                resp = await response.text()
                soup = BeautifulSoup(resp, "lxml")
                dct = {}

                author = soup.find('div', class_="caption--dIJlQ").get_text(strip=True)
                author_link = self.main_link + soup.find('a', class_="author--iD_jg")['href']
                title = soup.find('h1', class_="articleTitle--CCN0S").get_text(strip=True)
                body = soup.find('div', class_="articleView--s5exJ").get_text(strip=True)
                date = soup.find('div', class_="dateWrapper--ydt4b").get_text(strip=True)


                dct["author"] = author,
                dct["author_link"] = author_link,
                dct["title"] = title,
                dct["body"] = body
                dct["link_article"] = link
                dct["date_published"] = date


                self.tink_dict['Cat_articles'].append(dct)

    async def collect_info_articles(self, links_articles: list[str], cat_name: str, cat_link: str, headers: dict) -> None:

        self.tink_dict['Cat_name'] = cat_name
        self.tink_dict['Cat_link'] = cat_link
        self.tink_dict['Cat_articles'] = self.cat_articles

        async with aiohttp.ClientSession(headers=headers) as session:
                tasks = []
                for link in links_articles:
                    task = asyncio.create_task(self.collect_info_article(session=session, link=link, headers=headers))
                    tasks.append(task)
                await asyncio.gather(*tasks)

    def __call__(self, celery_task_id: str, list_hubs: str) -> None:
        new_task = Task.objects.create(celery_task_id=celery_task_id)
        print('list_hubs', list_hubs)
        print('list_hubs', list(list_hubs))
        for item in list(list_hubs):
            name = item['name_cat']
            link = item['link_cat']

            # we collect all articles from a hub and put them in json
            links_pages = self.get_links_articles(main_url=link, headers=self.head)
            asyncio.run(self.collect_info_articles(links_articles=links_pages, cat_name=name, cat_link=link, headers=self.head))
            # insert into db
            self.db.insert_authors(self.tink_dict)
            self.db.insert_articles(self.tink_dict)
        new_task.is_success = True
        new_task.save()

