import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from celery.result import AsyncResult
from .models import Category, Article, Task
from .serializers import ArticlesSerializer, CategorySerializer, TaskSerializer
from .tasks import collect_data_mel


logger = logging.getLogger('main')


class TaskViewSet(generics.ListAPIView):

    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class ArticleViewSet(generics.ListAPIView):

    queryset = Article.objects.all()
    serializer_class = ArticlesSerializer


class CategoryApiList(generics.ListCreateAPIView):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TaskMelInfo(generics.RetrieveAPIView):

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_object(self):
        celery_task_id = Task.objects.all().last().celery_task_id
        task_id = Task.objects.filter(celery_task_id=celery_task_id).first().id
        task_result = AsyncResult(str(task_id))
        result = {
            "task_id": task_id,
            "celery_task_id": celery_task_id,
            "task_status": task_result.status,
            "task_result": task_result.result
        }
        return result


@api_view(['POST'])
def parse_mel(request):

    """"The func can run the parser manually, without cron celery"""""

    if request.method == 'POST':

        try:
            collect_data_mel.delay()
            task_id = Task.objects.all().last().id
            task_id_celery = Task.objects.all().last().celery_task_id
            return Response({'Task was created': 200, 'Task_id': task_id, 'Task_id_celery': task_id_celery})

        except Exception as ex:

            return Response({'Internal Server Error': 500, 'Error': str(ex)})
    else:
        return Response({'This method is not allowed': 405})

