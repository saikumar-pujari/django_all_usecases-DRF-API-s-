from django.contrib.auth import get_user_model, login, logout, authenticate, SESSION_KEY, HASH_SESSION_KEY, BACKEND_SESSION_KEY
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_GET, require_POST
import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.sites.models import Site
from n1.models import (na, uuidmodel,)
from n1.utils.email import send_welcome_email


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


def send_email_view(request):
    send_welcome_email("receiver@gmail.com")
    return HttpResponse("Email sent!")


def get_from_request(request):
    name = request.GET.get('name', 'Guest')
    names = request.GET.get('names', 'Guest')
    return HttpResponse(f"Hello, {name} and {names=}!")


def my_view(request):
    # data = json.loads(request.body)
    # data = json.loads(request.method)
    print(f'request.method: {request.method}')
    print(f'request.body: {request.body}')
    print(f'request.content_type: {request.content_type}')
    # print(request.request)
    print(f'request.headers: {request.headers}')
    print(
        f'request.headers.get("User-Agent"): {request.headers.get("User-Agent")}')
    print(f'request.META: {request.META}')
    print(
        f'request.META.get("HTTP_USER_AGENT"): {request.META.get("HTTP_USER_AGENT")}')
    print(f'request.path: {request.path}')
    print(f'request.path_info: {request.path_info}')
    print(f'request.get_host(): {request.get_host()}')
    print(f'request.get_full_path(): {request.get_full_path()}')
    print(f'request.get_full_path_info(): {request.get_full_path_info()}')
    return HttpResponse(f"hey")


@csrf_exempt
def post_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(f"Received data: {data}")
        return HttpResponse("Data received!")
    else:
        return HttpResponse("Only POST requests are allowed.", status=405)
# def post_view(request):
#     data = json.loads(request.body)

#     name = data.get('name')
#     return HttpResponse(name)


def api_view(request):
    return JsonResponse({"name": "Sai"})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def all_view(request) -> HttpResponse:
    if request.method == 'GET':
        return HttpResponse("This is a GET request.")
    elif request.method == 'POST':
        # data = json.loads(request.body)
        # print(f"Received data: {data}")
        return HttpResponse("Data received!")
    return HttpResponse("This method is not allowed.", status=405)


# @require_POST
@csrf_exempt
@login_required
@permission_required(['n1.view_na', 'n1.change_na'], raise_exception=True)
# @permission_required('n1.view_na', )
def user_test(request):
    print(f"User: {request.user}")
    print(f"User is authenticated: {request.user.is_authenticated}")
    print(f"User is permissioned: {request.user.has_perm('n1.view_na')}")
    print(f"User is groups: {request.user.groups}")
    print(f"User is session: {request.session}")
    print(f"User is dict session: {dict(request.session)}")
    print(f"User is session key: {request.session.get(SESSION_KEY)}")
    return HttpResponse(f"user is {request.user.username} and email is {request.user.email}")


User = get_user_model()


@csrf_exempt
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if not username or not password:
            return HttpResponse("Username and password required")
        if User.objects.filter(username=username).exists():
            return HttpResponse("User already exists")
        User.objects.create_user(username=username, password=password)
        return HttpResponse("User registered successfully")
    return HttpResponse("Send POST request to register")


@csrf_exempt
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse(f"Logged in as {user.username}")
        return HttpResponse("Invalid credentials")
    return HttpResponse("Send POST request to login")


@login_required
def logout_view(request):
    logout(request)
    return HttpResponse("Logged out successfully")


@login_required
def dashboard(request):
    return HttpResponse(f"Welcome {request.user.username}")
