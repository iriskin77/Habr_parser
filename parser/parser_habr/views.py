from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Hub, Timer, Author, Texts
from .parser import ParserHub, Database
from .serializer import TextsSerializer, Authorerializer, HubSerializer
from rest_framework import viewsets, renderers
from .permissions import IsAdminOrReadOnly
import logging

logger = logging.getLogger('main')

class TextsViewSet(viewsets.ModelViewSet):

    queryset = Texts.objects.all()
    serializer_class = TextsSerializer
    permission_classes = (IsAdminOrReadOnly, )

class AuthorViewSet(viewsets.ModelViewSet):

    queryset = Author.objects.all()
    serializer_class = Authorerializer
    permission_classes = (IsAdminOrReadOnly, )

class HubViewSet(viewsets.ModelViewSet):

    queryset = Hub.objects.all()
    serializer_class = HubSerializer
    permission_classes = (IsAdminOrReadOnly, )

@api_view(['GET'])
def parse_habr(request):

    if request.method == 'GET':
        logger.info('Hello!')
        list_hubs = Hub.objects.all().values('hub_name', 'hub_link')
        pars = ParserHub()
        pars(list_hubs)
        return Response({'ok': 200})
    else:
        return Response({'This method is not allowed' : 405})
