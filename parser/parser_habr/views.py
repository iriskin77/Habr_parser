from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Hub, Timer, Author, Texts
from .parser import ParserHub, Database
from .serializer import TextsSerializer, Authorerializer, HubSerializer
from rest_framework import viewsets, renderers

class TextsViewSet(viewsets.ModelViewSet):

    queryset = Texts.objects.all()
    serializer_class = TextsSerializer

class AuthorViewSet(viewsets.ModelViewSet):

    queryset = Author.objects.all()
    serializer_class = Authorerializer

class HubViewSet(viewsets.ModelViewSet):

    queryset = Hub.objects.all()
    serializer_class = HubSerializer

@api_view(['GET', 'POST'])
def task(request):

    if request.method == 'GET':

        list_hubs = Hub.objects.all().values('hub_name', 'hub_link')
        pars = ParserHub()
        pars(list_hubs)

        return Response({'ok': 200})

        # with open(f"books24.json", "w", encoding="utf-8") as file:
        #       json.dump(pars.hub_dict, file, indent=4, ensure_ascii=False)
