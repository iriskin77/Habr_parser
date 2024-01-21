import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from celery.result import AsyncResult
from .permissions import IsAdminOrReadOnly
from .models import Hub, Author, Texts, Task
from .serializer import TextsSerializer, Authorerializer, HubSerializer, TaskSerializer
from .tasks import collect_data


logger = logging.getLogger('main')


class TaskViewSet(viewsets.ModelViewSet):

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAdminOrReadOnly, )


class TextsViewSet(viewsets.ModelViewSet):

    queryset = Texts.objects.all()
    serializer_class = TextsSerializer
    permission_classes = (IsAdminOrReadOnly, )


class AuthorViewSet(viewsets.ModelViewSet):

    queryset = Author.objects.all()
    serializer_class = Authorerializer
    permission_classes = (IsAdminOrReadOnly, )


class ListApiHub(ListAPIView):

    queryset = Hub.objects.all()
    serializer_class = HubSerializer
    permission_classes = (IsAdminOrReadOnly, )


@api_view(['POST'])
def add_habr_category(request):

    if request.method == 'POST':
        serialized_data = HubSerializer(data=request.data)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response({'status': 201, 'data': serialized_data.data})
        else:
            return Response({'error': serialized_data.errors})


@api_view(['POST'])
def parse_habr(request):

    if request.method == 'POST':

        try:
            collect_data.delay()
            task_id = Task.objects.all().last().id
            task_id_celery = Task.objects.all().last().celery_task_id

            return Response({'Task was created': 200, 'Task_id': task_id, 'Task_id_celery': task_id_celery})

        except Exception as ex:
            return Response({'Internal Server Error': 500, 'Error': str(ex)})
    else:
        return Response({'This method is not allowed': 405})


@api_view(['GET'])
def get_task_habr_info(request):

    if request.method == 'GET':

        celery_task_id = Task.objects.all().last().celery_task_id
        task_id = Task.objects.filter(celery_task_id=celery_task_id).first().id
        task_result = AsyncResult(str(task_id))
        result = {
            "task_id": task_id,
            "celery_task_id": celery_task_id,
            "task_status": task_result.status,
            "task_result": task_result.result
        }
        return Response(result)
    else:
        return Response({"This method is not allowed": 405})


