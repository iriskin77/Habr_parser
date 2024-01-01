from bs4 import BeautifulSoup
import requests
from aiohttp_retry import RetryClient, ExponentialRetry
import aiohttp
import asyncio
from apps.parser_mel.models import Task

headers = {
        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Cookie': 'news_lang=ru; yandex_login=talcore; ys=udn.cDrQktC70LDQtNC40YHQu9Cw0LIg0JrQsNGA0L/QtdC90LrQvg%3D%3D#c_chck.3181849896; yandexuid=7355079031598165761; mda2_beacon=1672991591886; gdpr=0; _ym_uid=1668166334590200044; addruid=J16Al8s1i5J74M9S9pL5k1W1f9; Session_id=3:1684046607.5.0.1672991591876:1DI8uQ:15a.1.2:1|552541704.0.2|64:10009557.333765.bRabFjTPl-KB0YFwm7thxr4P1Eg; sessionid2=3:1684046607.5.0.1672991591876:1DI8uQ:15a.1.2:1|552541704.0.2|64:10009557.333765.fakesign0000000000000000000; tmr_lvid=25aa36deb66ec3f5fd31de74352c56df; tmr_lvidTS=1665515375244; _ym_d=1693207925; Zen-User-Data={%22zen-theme%22:%22light%22}; zen_sso_checked=1; rec-tech=true; _ym_isad=1; KIykI=1; crookie=GwkL3T35JZAFN7/LgkLy5B06+N//nBiHRavbYemTc3SQ283H5odlLAaFAbEviWDO04s3S8SNGtCpq/kPhcdHkItBFYI=; cmtchd=MTY5NjMwODI2NzIwOQ==; _yasc=NEEDPcWQa1OaQo640rfL6v+8e9D3HVcXi8nYWOEebBJActfjCMY2F5mAmVGLC8g6; bltsr=1; tmr_detect=1%7C1696312690921',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    }


class ParserMel:

    res_dict = {}

    main = "https://mel.fm"

    def get_articles(self, main_url: str, head: dict) -> list[str]:
        resp = requests.get(url=main_url, headers=head)
        soup = BeautifulSoup(resp.text, "lxml")
        links = soup.find_all('a', class_="b-pb-article-card__link")
        links_articles = [self.main + link["href"] for link in links]
        return links_articles

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

                    self.res_dict["Mel_Article"].append({
                        'title': title,
                        'body': body,
                        'link_article': link,
                        'date_published': date,
                    })
        except:
            print("error")

    async def collect_info_articles(self, links: list[str], head: dict, mel_cat: str, mel_cat_link: str) -> None:

        self.res_dict["Mel_cat"] = mel_cat
        self.res_dict["Mel_cat_link"] = mel_cat_link
        self.res_dict["Mel_Article"] = []

        async with aiohttp.ClientSession(headers=headers) as session:
            tasks = []
            for link in links:
                task = asyncio.create_task(self.collect_info_article(session=session, link=link, head=head))
                tasks.append(task)
            await asyncio.gather(*tasks)

    def __call__(self, celery_task_id: str, list_cat: str) -> None:
        new_task = Task.objects.create(celery_task_id=celery_task_id)
        for item in list(list_cat):
            name = item['name_cat']
            link_cat = item['link_cat']

            links = self.get_articles(main_url=link_cat, head=headers)
            asyncio.run(self.collect_info_articles(links, headers, name, link_cat))
            self.db.insert_authors(self.tink_dict)
            self.db.insert_articles(self.tink_dict)
        new_task.is_success = True
        new_task.save()
