from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def hello(request):
    print(request.resolver_match.app_name)
    return HttpResponse("saikumar")
