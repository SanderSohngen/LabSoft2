from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<patient_id>\d+)/(?P<profession>\w+)/(?P<professional_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
]