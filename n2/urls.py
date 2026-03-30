from django.urls import path
from n2.views import *
urlpatterns = [
    path('b', hello),
]
