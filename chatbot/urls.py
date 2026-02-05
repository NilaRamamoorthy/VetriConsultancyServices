from django.urls import path
from .views import chatbot_reply,ask_view,chatbot_greeting_view

app_name = 'chatbot'

urlpatterns = [
    path('reply/', chatbot_reply, name='reply'),
    path('ask/', ask_view, name='ask'),
    path('greeting/', chatbot_greeting_view, name='greeting'),
]
