from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions
from rest_framework import reverse
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import detail_route

from .permissions import IsOwnwerOrReadOnly
from .models import Snippet
from .serializers import SnippetSerializer, UserSerializer

# Create your views here.



@api_view(['GET', 'POST'])
def snippet_list(request, format = None):
    '''
    List all code snippets, or create a new snippet
    '''
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many = True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format = None):
    '''
    Retrieve, update or delete a code snippet
    '''

    try:
        snippet = Snippet.objects.get(pk=pk)
    except:
        return Response(status = status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)


class SnippetList(generics.ListCreateAPIView):
    '''List all api views or create a new snippet'''
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)

    # def get(self, request, *args, **kwargs):
    #     # snippets = Snippet.objects.all()
    #     # serializer = SnippetSerializer(snippets, many = True)
    #     # return Response(serializer.data)
    #     return self.list(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     # serializer = SnippetSerializer(data=request.data)
    #     # if serializer.is_valid():
    #     #     serializer.save()
    #     #     return Response(serializer.data, status = status.HTTP_201_CREATED)
    #     # return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    #     return self.create(request, *args, **kwargs)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    '''
    Retrieve, update or delete a snippet instance
    '''
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnwerOrReadOnly,)

    # # def get_object(self, pk):
    # #     try:
    # #         return Snippet.objects.get(pk=pk)
    # #     except Snippet.DoesNotExist:
    # #         raise Http404

    # def get(self, request, *args, **kwargs):
    #     # snippet = self.get_object(pk)
    #     # serializer = SnippetSerializer(snippet)
    #     # return Response(serializer.data)
    #     return self.retrieve(request, *args, **kwargs)

    # def put(self, request, *args, **kwargs):

    #     # snippet =  self.get_object(pk)
    #     # serializer = SnippetSerializer(snippet, data=request.data)
    #     # if serializer.is_valid():
    #     #     serializer.save()
    #     #     return Response(serializer.data)
    #     # return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    #     return self.update(request, *args, **kwargs)
    # def delete(self, request, *args, **kwargs):
    #     # snippet = self.get_object(pk)
    #     # snippet.delete()
    #     # return Response(status =status.HTTP_204_NO_CONTENT)
    #     return self.destroy(request, *args, **kwargs)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer



@api_view(('GET',))
def api_root(request, format = None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })

class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    This class Automatically provides `list` and `detail` actions
    '''

    queryset = User.objects.all()
    serializer_class = UserSerializer

class SnippetViewSet(viewsets.ModelViewSet):
    '''
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy actions
    '''
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnwerOrReadOnly)

    @detail_route(renderer_classes = [renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)
































