import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from celery.result import AsyncResult
from rest_framework.generics import ListAPIView
from .permissions import IsAdminOrReadOnly
from .models import Category, Article, Task
from .serializers import ArticlesSerializer, CategorySerializer, TaskSerializer
from .tasks import collect_data_mel


logger = logging.getLogger('main')


class TaskViewSet(viewsets.ModelViewSet):

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAdminOrReadOnly, )


class ArticleViewSet(viewsets.ModelViewSet):

    queryset = Article.objects.all()
    serializer_class = ArticlesSerializer
    permission_classes = (IsAdminOrReadOnly, )


class CategoryApiList(ListAPIView):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly, )


@api_view(['POST'])
def add_mel_category(request):

    if request.method == 'POST':

        serialized_data = CategorySerializer(data=request.data)
        if serialized_data.is_valid():
            new_mel_name = serialized_data.validated_data['name_cat']
            new_mel_link = serialized_data.validated_data['link_cat']
            check_name = Category.objects.filter(name_cat=new_mel_name).exists()
            check_link = Category.objects.filter(link_cat=new_mel_link).exists()
            if not check_name and not check_link:
                Category.objects.create(name_cat=new_mel_name, link_cat=new_mel_link).save()
                return Response({'status': 201, 'data': serialized_data.data})
            else:
                return Response({'status': 304})
        else:
            return Response({'error': serialized_data.errors})


@api_view(['POST'])
def parse_mel(request):

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


@api_view(['GET'])
def get_task_info_mel(request):

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


