import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from celery.result import AsyncResult
from .models import Hub, Author, Texts, Task
from .serializer import TextsSerializer, AuthorSerializer, HubSerializer, TaskSerializer
from .tasks import collect_data_habr


logger = logging.getLogger('main')


class TaskViewSet(generics.ListAPIView):

    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TextsViewSet(generics.ListAPIView):

    queryset = Texts.objects.all()
    serializer_class = TextsSerializer


class AuthorViewSet(generics.ListAPIView):

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class ListApiHub(generics.ListAPIView):

    queryset = Hub.objects.all()
    serializer_class = HubSerializer


class AddCategory(generics.ListCreateAPIView):

    queryset = Hub.objects.all()
    serializer_class = HubSerializer


class TaskHabrInfo(generics.RetrieveAPIView):

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
def parse_habr(request):

    """"The func can run the parser manually, without cron celery"""""

    if request.method == 'POST':

        try:
            collect_data_habr.delay()
            task_id = Task.objects.all().last().id
            task_id_celery = Task.objects.all().last().celery_task_id
            # 'Task_id': task_id, 'Task_id_celery': task_id_celery
            return Response({'Task was created': 200,
                             'Task_id': task_id,
                             'Task_id_celery': task_id_celery})

        except Exception as ex:
            return Response({'Internal Server Error': 500, 'Error': str(ex)})
    else:
        return Response({'This method is not allowed': 405})

