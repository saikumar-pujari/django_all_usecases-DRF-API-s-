from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.sites.models import Site
from n1.models import *


def hello(request):
    return HttpResponse("sai")


def nab(req, **kw):
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
    # p=na.objects.get(id=1)
    # p = list(na.objects.all())
    p = na.objects.all().order_by()[:50]
    # p = na.objects.only('name')
    # p = na.objects.values('name').iterator()
    # p = na.objects.values('name')[:50]
    # p = na.objects.values_list('name', flat=True)
    context = {
        'name': 'sai',
        'age': 22,
        'lang': 'python',
        'skills': ['django', 'flask', 'fastapi', {'frontend': ['react', 'vue', 'angular']}],
        'post': p,
        'colors': ["Red", "Blue", "Green"]
    }

    return render(req, '1.html', context)


def uuid(req, uuid):
    p = uuidmodel.objects.get(id=uuid)
    print(p.id)
    print(p.name)
    return HttpResponse(p.name)
