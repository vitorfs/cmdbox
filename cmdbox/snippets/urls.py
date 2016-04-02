from django.conf.urls import url

from cmdbox.snippets import views


urlpatterns = [
    url(r'add/$', views.add, name='add'),
    url(r'^(?P<username>[^/]+)/(?P<slug>[^/]+)/$', views.snippet, name='snippet'),
    url(r'^(?P<username>[^/]+)/(?P<slug>[^/]+)/edit/$', views.edit, name='edit'),
    url(r'^(?P<username>[^/]+)/(?P<slug>[^/]+)/delete/$', views.delete, name='delete'),
]
