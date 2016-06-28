from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^create/$', views.post_edit, name='post_create'),
    url(r'^edit/(?P<post_id>\d+)/$', views.post_edit, name='post_edit'),
    url(r'^detail/(?P<post_id>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^send_comment/(?P<post_id>\d+)/$', views.send_comment, name='send_comment'),
    url(r'^post_remove/(?P<post_id>\d+)/$', views.post_remove, name='post_remove'),
    url(r'^comment_remove/(?P<comment_id>\d+)/$', views.comment_remove, name='comment_remove'),
]