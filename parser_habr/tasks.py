from .models import Hub, Task
from .pars_habr import ParserHub, Database
from parser.celery import app
from .models import Hub


#name='create_task', bind=True


@app.task(name='create_task', bind=True)
def collect_data(self):
    #logger.info(f'Fn {create_task.__name__}. The task was created')
    #print('create_task works')
    list_hubs = Hub.objects.all().values('hub_name', 'hub_link')
    pars = ParserHub()
    pars(celery_task_id=self.request.id, list_hubs=list_hubs)
    #parse_data(self.request.id, category_name)
    return True
