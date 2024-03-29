from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^new$', views.NewListView.as_view(), name='new_list'),
    re_path(r'^(?P<pk>\d+)/$', views.ViewAndAddToListView.as_view(), name='view_list'),
    re_path(r'^users/(.+)/$', views.my_lists, name='my_lists'),
    re_path(r'^(\d+)/share/$', views.share_list, name='share'),
]
