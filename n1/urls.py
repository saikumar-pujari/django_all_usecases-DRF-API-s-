from django.urls import path, re_path
from n1.views import *
urlpatterns = [
    path('a', hello),
    path('b/<str:name>/', na),
    path('c/<str:name>/<str:kw>/', na),
    path('e/', n),
    path('1/', a),
]
