from apps.parser_tink.parser.parser_tink import Parser
from parser.celery import app
from .models import Category
from apps.parser_mel.parser.parser_mel import ParserMel


#name='create_task', bind=True


@app.task(name='create_task_mel', bind=True)
def collect_data_mel(self):
    #logger.info(f'Fn {create_task.__name__}. The task was created')
    #print('create_task works')
    list_items = Category.objects.all().values('name_cat', 'link_cat')
    mel_pars = ParserMel()
    mel_pars(celery_task_id=self.request.id, list_cat=list_items)
    #parse_data(self.request.id, category_name)
    return True
