from django.conf.urls import url

from cmdbox.core import views as core_views


urlpatterns = [
    url(r'^$', core_views.home, 'home')
]
