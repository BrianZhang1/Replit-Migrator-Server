from django.urls import path
from .views import data_handler, registration_handler, delete_user_handler, chat_handler

urlpatterns = [
    path('api/', data_handler),
    path('delete-user-data/', delete_user_handler),
    path('register/', registration_handler),
    path('chat/', chat_handler)
]
