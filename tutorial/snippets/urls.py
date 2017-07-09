from django.conf.urls import url, patterns, include
from rest_framework.urlpatterns import format_suffix_patterns
#from snippets import views
#from snippets.views import SnippetViewSet, UserViewSet, api_root
from rest_framework import renderers
from snippets import views
from rest_framework.routers import  DefaultRouter
from rest_framework_swagger.views import  get_swagger_view

#schema_view = get_schema_view(title="Pastebin API")
schema_view = get_swagger_view(title="Pastebin API", url='/snippets')


#set Set the specific method
#Don't forget .as_view
'''
snippet_list = SnippetViewSet.as_view({
	'get' : 'list',
	'post' : 'create'
})

snippet_detail = SnippetViewSet.as_view({
	'get' : 'retrieve',
	'put' : 'update',
	'patch' : 'partial_update',
	'delete' : 'destroy'
})

snippet_hightlight = SnippetViewSet.as_view({
	'get' : 'highlight'
}, renderer_classes = [renderers.StaticHTMLRenderer])
#specific renderer_class

user_list = UserViewSet.as_view({
	'get': 'list'
})

user_detail = UserViewSet.as_view({
	'get' : 'retrieve'
})


urlpatterns = [
	url(r'^$', api_root),
	#url(r'^snippets/(?P<pk>[0-9]+)/highlight/$', views.SnippetHighlight.as_view()),
	url(r'^snippets/$', snippet_list, name = 'snippet-list'),
	url(r'^snippets/(?P<pk>[0-9]+)/$', snippet_detail, name='snippet-detail'),
	url(r'^snippets/(?P<pk>[0-9]+)/highlight/$', snippet_hightlight, name='snippet-highlight'),
	url(r'^users/$', user_list, name = 'user-list'),
	url(r'^users/(?P<pk>[0-9]+)/$', user_detail, name = 'user-detail'),
    url(r'^schema/$', schema_view),
]

urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns += [url(r'^api-auth/', include('rest_framework.urls',  namespace = 'rest_framework')),]

'''



router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    url(r'^', schema_view),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^schema/$', schema_view),
]
