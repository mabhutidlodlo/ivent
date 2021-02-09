
from django.urls import re_path

from . import consumer

websocket_urlpatterns = [
    re_path(r'wss/notify/(?P<id>[0-9]+)/(?P<token>\w+)/$', consumer.NotificationConsumer),
]
