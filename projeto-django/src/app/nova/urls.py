from django.urls import path
from . import views

app_name = 'nova'

urlpatterns = [
    path('chat/documento/<uuid:doc_pk>/', views.start_chat_from_doc, name='start_chat'),
    path('chat/<uuid:session_id>/', views.chat_session_view, name='chat_session'),
    path('chat/<uuid:session_id>/send/', views.send_message_api, name='send_message_api'),
]
