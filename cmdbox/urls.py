from django.conf.urls import url
from django.contrib.auth import views as auth_views

from cmdbox.core import views as core_views
from cmdbox.snippets import views as snippets_views
from cmdbox.profiles import views as profiles_views

urlpatterns = [
    url(r'^$', core_views.home, name='home'),
    url(r'^login/$', auth_views.login, {'template_name': 'core/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^settings/$', profiles_views.account_settings, name='account_settings'),
    url(r'^password/$', profiles_views.change_password, name='change_password'),
    url(r'^(?P<username>[^/]+)/$', snippets_views.snippets, name='snippets'),
]
