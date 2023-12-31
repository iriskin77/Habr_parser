import logging
from apps.parser_tink.models import Article, Category, Author


class Database:

    def __init__(self):
        self.logger = logging.getLogger('main')

    def insert_authors(self, json_articles: dict) -> None:

        for article in json_articles['Cat_articles']:
                author_check = Author.objects.filter(author=article['author'][0]).exists()
                if not author_check:
                    Author.objects.create(author=article['author'][0], author_link=article['author_link'][0]).save()

    def insert_articles(self, json_articles: dict) -> None:

         for article in json_articles['Cat_articles']:

                cat_name = Category.objects.filter(name_cat=json_articles['Cat_name']).first()
                author = Author.objects.filter(author=article['author'][0]).first()

                article_check = Article.objects.filter(title=article['title'][0]).exists()

                if not article_check:

                    new_text = Article.objects.create(
                                         category=cat_name,
                                         author=author,
                                         title=article['title'][0],
                                         body=article['body'],
                                         date_published=article['date_published'],
                                         link=article['link_article']
                    )
                    new_text.save()

