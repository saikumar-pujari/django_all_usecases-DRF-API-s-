from django.urls import path
from n2.views import *
app_name = "n2"
urlpatterns = [
    path('b', hello),
]
