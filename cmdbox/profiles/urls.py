from django.conf.urls import url

from cmdbox.profiles import views


urlpatterns = [
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^account/$', views.account, name='account'),
    url(r'^password/$', views.password, name='password'),
    url(r'^logins/$', views.logins, name='logins'),
]
