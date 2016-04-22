from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from cmdbox.core import views as core_views
from cmdbox.snippets import views as snippets_views
from cmdbox.scaffold_templates import views as scaffold_templates_views


urlpatterns = [
    url(r'^$', core_views.home, name='home'),
    url(r'^oauth/', include('social.apps.django_app.urls', namespace='social')),
    url(r'^login/$', auth_views.login, {'template_name': 'core/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^settings/', include('cmdbox.profiles.urls', namespace='settings')),
    url(r'^snippets/$', snippets_views.index, name='snippets'),
    url(r'^snippets/add/$', snippets_views.add, name='add_snippet'),
    url(r'^scaffold-templates/$', scaffold_templates_views.index, name='scaffold_templates'),
    url(r'^scaffold-templates/add/$', scaffold_templates_views.add, name='add_scaffold_template'),
    url(r'^help/', include('cmdbox.help.urls', namespace='help')),
    url(r'^(?P<username>[^/]+)/$', core_views.profile, name='profile'),
    url(r'^(?P<username>[^/]+)/snippets/', include('cmdbox.snippets.urls', namespace='snippets')),
    url(r'^(?P<username>[^/]+)/scaffold-templates/',
        include('cmdbox.scaffold_templates.urls', namespace='scaffold_templates')),
    url(r'', include('cmdbox.api.urls', namespace='api'))
]
