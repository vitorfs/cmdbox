from django.conf.urls import url

from cmdbox.scaffold_templates import views


urlpatterns = [
    url(r'^$', views.scaffold_templates, name='list'),
    url(r'^(?P<slug>[^/]+)/$', views.details, name='details'),
    url(r'^(?P<slug>[^/]+)/add-file/$', views.add_file, name='add_file'),
    url(r'^(?P<slug>[^/]+)/(?P<folder_id>\d+)/add-file/$', views.add_children_file, name='add_children_file'),
    url(r'^(?P<slug>[^/]+)/edit/$', views.edit, name='edit'),
    url(r'^(?P<slug>[^/]+)/delete/$', views.delete, name='delete'),
]
