import logging
from apps.parser_habr.models import Texts, Author, Hub


class Database:

    def __init__(self):
        self.logger = logging.getLogger('main')

    def insert_authors(self, json_articles: dict) -> None:
        """"Input: json with all articles from a hub. Output: the function inserts author-name and author-link in db"""""

        self.logger.info(f'Fn {self.insert_authors.__name__} has started')

        try:
            for article in json_articles['Hub_articles']:

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
