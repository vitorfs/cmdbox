from django.conf.urls import url

from cmdbox.scaffold_templates import views


urlpatterns = [
    url(r'^$', views.scaffold_templates, name='list'),
    url(r'^(?P<slug>[^/]+)/$', views.details, name='details'),
    url(r'^(?P<slug>[^/]+)/add-file/$', views.add_file, name='add_file'),
    url(r'^(?P<slug>[^/]+)/add-folder/$', views.add_folder, name='add_folder'),
    url(r'^(?P<slug>[^/]+)/(?P<file_id>\d+)/add-file/$', views.add_children_file, name='add_children_file'),
    url(r'^(?P<slug>[^/]+)/(?P<file_id>\d+)/add-folder/$', views.add_children_folder,
        name='add_children_folder'),
    url(r'^(?P<slug>[^/]+)/(?P<file_id>\d+)/rename/$', views.rename_file, name='rename_file'),
    url(r'^(?P<slug>[^/]+)/(?P<file_id>\d+)/duplicate/$', views.duplicate_file, name='duplicate_file'),
    url(r'^(?P<slug>[^/]+)/(?P<file_id>\d+)/delete/$', views.delete_file, name='delete_file'),
    url(r'^(?P<slug>[^/]+)/edit/$', views.edit, name='edit'),
    url(r'^(?P<slug>[^/]+)/edit/(?P<file_id>\d+)/$', views.edit_file, name='edit_file'),
    url(r'^(?P<slug>[^/]+)/delete/$', views.delete, name='delete'),
]
