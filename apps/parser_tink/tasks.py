from apps.parser_tink.parser.parser_tink import Parser
from parser.celery import app
from .models import Category


@app.task(bind=True)
def collect_data_tinkoff(self):
    list_hubs = Category.objects.all().values('name_cat', 'link_cat')
    pars = Parser()
    pars(celery_task_id=self.request.id, list_hubs=list_hubs)
    return True
