from apps.parser_tink.parser.parser_tink import Parser
from parser.celery import app
from .models import Category
from apps.parser_mel.parser.parser_mel import ParserMel


@app.task(bind=True)
def collect_data_mel(self):
    list_items = Category.objects.all().values('name_cat', 'link_cat')
    print(list_items)
    mel_pars = ParserMel()
    mel_pars(celery_task_id=self.request.id, list_cat=list_items)
    return True
