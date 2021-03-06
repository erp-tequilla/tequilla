from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.dialog_list, name='dialog_list'),
    url(r'^send_message/$', views.send_message, name='send_message'),
    url(r'^resend_messages/$', views.resend_messages, name='resend_messages'),
    url(r'^show_dialog/(?P<with_user_id>\d+)/$', views.show_dialog, name='show_dialog'),
    url(r'^get_last_messages/(?P<with_user_id>\d+)/$', views.get_last_messages, name='get_last_messages'),
    url(r'^remove_message/(?P<message_id>\d+)/$', views.remove_message, name='remove_message'),
]
