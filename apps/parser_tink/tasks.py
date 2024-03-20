from apps.parser_tink.parser.parser_tink import Parser
from parser.celery import app
from .models import Category


@app.task(bind=True)
def collect_data_tinkoff(self):
    list_hubs = Category.objects.all().values('name_cat', 'link_cat')
    pars = Parser()
    print('collect_data_tinkoff', list_hubs)
    pars(list_hubs=list_hubs)
    return True
