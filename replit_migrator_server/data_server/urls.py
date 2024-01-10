from django.urls import path
from .views import data_handler, registration_handler

urlpatterns = [
    path('api/', data_handler),
    path('register/', registration_handler)
]
