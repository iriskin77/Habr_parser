import logging
from apps.parser_tink.models import Article, Category, Author


class Database:

    def __init__(self):
        self.logger = logging.getLogger('main')

    def insert_authors(self, json_articles: dict) -> None:
        self.logger.info(f'Fn insert_authors has started')
        try:
            for article in json_articles['Mel_articles']:
                author_check = Author.objects.filter(author=article['author']).exists()
                if not author_check:
                    Author.objects.create(author=article['author']).save()
        except:
            self.logger.info(f'Fn insert_authors has finished incorrectly')


    def insert_articles(self, json_articles: dict) -> None:
        self.logger.info(f'Fn insert_articles has started')
        try:
            for article in json_articles['Mel_articles']:

                cat_name = Category.objects.filter(name_cat=json_articles['Mel_cat']).first()
                author = Author.objects.filter(author=article['author']).first()

                article_check = Article.objects.filter(title=article['title']).exists()

                if not article_check:

                    new_text = Article.objects.create(
                                         category=cat_name,
                                         author=author,
                                         title=article['title'],
                                         body=article['body'],
                                         date_published=article['date_published'],
                                         link=article['link_article']
                    )
                    new_text.save()
        except:
            self.logger.info(f'Fn insert_articles has finished incorrectly')

