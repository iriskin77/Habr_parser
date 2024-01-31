from apps.parser_habr.parser.pars_habr import ParserHub
from parser.celery import app
from apps.parser_habr.models import Hub


@app.task(bind=True)
def collect_data_habr(self):
    list_hubs = Hub.objects.all().values('hub_name', 'hub_link')
    pars = ParserHub()
    pars(celery_task_id=self.request.id, list_hubs=list_hubs)
    return True
