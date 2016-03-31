from django.conf.urls import url

from cmdbox.snippets import views


urlpatterns = [
    url(r'add/$', views.add, name='add'),
    url(r'^(?P<username>[^/]+)/(?P<slug>[^/]+)/$', views.snippet, name='snippet'),
]
