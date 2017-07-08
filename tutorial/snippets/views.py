
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer
from snippets.permissions import IsOwnerOrReadOnly
from django.http import Http404
from rest_framework import generics
from rest_framework import permissions
from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework import renderers
# Create your views here.

#Version - 1
'''
@api_view(['GET', 'POST'])
def snippet_list(request, format = None):
	if request.method == 'GET':
		snippets = Snippet.objects.all()
		serializer = SnippetSerializer(snippets, many = True)
		return Response(serializer.data)

	elif request.method == 'POST':
		serializer = SnippetSerializer(data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status = status.HTTP_201_CREATED)
		return JsonResponse(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
'''
'''
@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format = None):
	try:
		snippet = Snippet.objects.get(pk = pk)
	except Snippet.DoesNotExist:
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
'''
#Version - 2
'''
class SnippetList(APIView):
	def get(self, request, format = None):
		snippets = Snippet.objects.all()
		serializer = SnippetSerializer(snippets, many = True)
		return Response(serializer.data)

	def post(self, request, format = None):
		serializer = SnippetSerializer(data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status = status.HTTP_201_CREATED)
		return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class SnippetDetail(APIView):
	def GetObject(self, pk):
		try:
			return Snippet.objects.get(pk = pk)
		except Snippet.DoesNotExist:
			raise Http404

	def get(self, request, pk, format = None):
		snippet = self.GetObject(pk) #get certain object in db
		serializer = SnippetSerializer(snippet)
		return Response(serializer.data)

	def put(self, request, pk, format = None):
		snippet = self.GetObject(pk)
		serializer = SnippetSerializer(snippet, data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data) #return modified data
		return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format = None):
		snippet = self.GetObject(pk)
		snippet.delete()
		return Response(status = status.HTTP_204_NO_CONTENT)
'''

#Version - 3

@api_view(['GET'])
def api_root(request, format = None):
	return Response({
		'users': reverse('user-list', request=request, format=format),
		'snippets' : reverse('snippet-list', request = request, format = format)
	})


class SnippetHighlight(generics.GenericAPIView):
	queryset = Snippet.objects.all()
	renderer_classes = (renderers.StaticHTMLRenderer,)

	def get(self, request, *args, **kwargs):
		snippet = self.get_object()
		return Response(snippet.highlighted)

class SnippetList(generics.ListCreateAPIView):
	queryset = Snippet.objects.all()
	serializer_class  = SnippetSerializer # declare serizlizerClass 
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
	def perform_create(self, serializer):
		serializer.save(owner = self.request.user) #record user

class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, )
	queryset = Snippet.objects.all()
	serializer_class  = SnippetSerializer 


class UserList(generics.ListAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView): #just retrieve
	queryset = User.objects.all()
	serializer_class = UserSerializer