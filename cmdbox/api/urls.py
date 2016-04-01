from django.conf.urls import url

from cmdbox.api import views


urlpatterns = [
    url(r'^(?P<username>[^/]+)/(?P<slug>[^/]+)/$', views.snippet, name='snippet'),
]
