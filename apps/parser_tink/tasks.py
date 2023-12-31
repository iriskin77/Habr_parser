from apps.parser_tink.parser.parser_tink import Parser
from parser.celery import app
from .models import Category


#name='create_task', bind=True


@app.task(name='create_task_tink', bind=True)
def collect_data_tinkoff(self):
    #logger.info(f'Fn {create_task.__name__}. The task was created')
    #print('create_task works')
    list_hubs = Category.objects.all().values('name_cat', 'link_cat')
    pars = Parser()
    pars(celery_task_id=self.request.id, list_hubs=list_hubs)
    #parse_data(self.request.id, category_name)
    return True
