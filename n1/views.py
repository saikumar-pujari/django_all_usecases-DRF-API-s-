from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.contrib.sites.models import Site


def hello(request):
    return HttpResponse("sai")


def na(req, **kw):
    context = {'status': 'naman!'}
    print(kw.get('name'))
    print(kw.get('year'))
    print(kw)
    n = tuple(kw.values())
    print(n)
    # return HttpResponse("naman"+str(kw)+str(context))
    # return HttpResponse("naman"+str(kw))
    if len(n) > 1:
        return HttpResponse(str(kw)+str(n[0])+str(n[1]))
    elif len(n) > 0:
        return HttpResponse(str(kw)+str(n[0]))
    else:
        return HttpResponse(str(kw))


def n(req):
    current_site = Site.objects.get_current()
    return HttpResponse(current_site.domain)


def a(req):
    context = {
        'name': 'sai',
        'age': 22,
        'lang': 'python',
        'skills': ['django', 'flask', 'fastapi', {'frontend': ['react', 'vue', 'angular']}]
    }
    return render(req, '1.html', context)
