from django.conf.urls import url

from cmdbox.help import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
]
