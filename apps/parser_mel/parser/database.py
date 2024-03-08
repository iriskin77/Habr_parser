import logging
from apps.parser_mel.models import Article, Category


class Database:

    def __init__(self):
        self.logger = logging.getLogger('main')

    def insert_articles(self, json_articles: dict) -> None:
        self.logger.info(f'Fn insert_articles has started')
        try:
            for article in json_articles['Mel_articles']:

                cat_name = Category.objects.filter(name_cat=json_articles['Mel_cat']).first()

                new_text = Article.objects.create(
                                         category=cat_name,
                                         title=article['title'],
                                         body=article['body'],
                                         date_published=article['date_published'],
                                         link=article['link_article']
                    )
                new_text.save()
            self.logger.info(f'Fn insert_articles. Articles were inserted successfully')
        except:
            self.logger.info(f'Fn insert_articles has finished incorrectly')

