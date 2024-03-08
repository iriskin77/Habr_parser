import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from celery.result import AsyncResult
from .models import Category, Author, Article, Task
from .serializers import ArticlesSerializer, CategorySerializer, TaskSerializer, AuthorSerializer
from .tasks import collect_data_tinkoff
from rest_framework import generics


logger = logging.getLogger('main')


class TaskViewSet(generics.ListAPIView):

    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class ArticleViewSet(generics.ListAPIView):

    queryset = Article.objects.all()
    serializer_class = ArticlesSerializer


class AuthorViewSet(generics.ListAPIView):

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class CategoryApiList(generics.ListAPIView):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@api_view(['POST'])
def add_tink_category(request):

    """"The func enables to add a new category into db"""""

    if request.method == 'POST':

        serialized_data = CategorySerializer(data=request.data)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response({'status': 201, 'data': serialized_data.data})
        else:
            return Response({'error': serialized_data.errors})
    else:
        return Response({'This method is not allowed': 405})


@api_view(['POST'])
def parse_tink(request):

    """"The func can run the parser manually, without cron celery"""""

    if request.method == 'POST':

        try:
            collect_data_tinkoff.delay()
            task_id = Task.objects.all().last().id
            task_id_celery = Task.objects.all().last().celery_task_id
            return Response({'Task was created': 201, 'Task_id': task_id, 'Task_id_celery': task_id_celery})

        except Exception as ex:

            return Response({'Internal Server Error': 500, 'Error': str(ex)})
    else:
        return Response({'This method is not allowed': 405})


@api_view(['GET'])
def get_task_info(request):

    """"The func enables to get info about the running parser"""""

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


