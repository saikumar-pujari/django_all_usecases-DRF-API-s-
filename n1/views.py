# from n1.redis_client import redis_client
from .pagination import (CustomPagination, limitpagination,CursorPagination)
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .throttle import (loginthrottle, notloggedinthrottle)
from rest_framework.throttling import (
    UserRateThrottle, AnonRateThrottle, ScopedRateThrottle)
from rest_framework.decorators import api_view
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.generics import (GenericAPIView, ListAPIView, ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView)
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin
)
from rest_framework.views import APIView
from rest_framework.response import Response
from .serlizer import (naSerializer, booksSerializer,
                       authorsSerializer, BookSerializer, userSerializer)
from django.core.serializers import serialize
from sqlparse import format
from django.db import connection
from typing import Any
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.utils.decorators import method_decorator
from django.views import View
from django.urls import reverse
from django.core.signing import Signer, BadSignature
from asgiref.sync import sync_to_async, async_to_sync
import time
import logging
import json
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model, login, logout, authenticate, SESSION_KEY, HASH_SESSION_KEY, BACKEND_SESSION_KEY
from django.contrib.auth.decorators import permission_required, login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_GET, require_POST, condition, last_modified
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.sites.models import Site
from n1.models import (na, user, uuidmodel, usser, data, book, autor)
from n1.utils.email import send_welcome_email
from n1.signals import custom_signal


def hello(request):
    print(f"Request IP: {request.META.get('REMOTE_ADDR')}")
    # print(request.META)
    print(f"View Name: {request.resolver_match.view_name}")
    print(f"URL Name: {request.resolver_match.url_name}")
    print(f"App Name: {request.resolver_match.app_name}")
    print(f"Namespaces: {request.resolver_match.namespaces}")
    print(f"Route: {request.resolver_match.route}")
    match = request.resolver_match
    if match and match.app_name == "n1":
        print("Matched n1 app")
    print(f'session_key: {request.session.session_key}')
    # print(request.session.create()) #is session is not created then it will create session and return session key otherwise it will return None
    # print(f'session_key: {request.session.session_key}')
    # print(request.session.create())
    # print(f'session_key: {request.session.session_key}')
    return HttpResponse(json.dumps(dict(request.META), default=str), content_type="application/json")


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
    print(list(connection.queries))
    p = ((connection.queries[-1]['time']))
    print(p)
    print("Total queries:", len(connection.queries))
    print("Total time:", sum(float(q['time']) for q in connection.queries))
    q = list(connection.queries)
    for query in q:
        print(format(query['sql'], reindent=True, keyword_case='upper'))
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


# def api_view(request):
#     return JsonResponse({"name": "Sai"})


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
    site = get_current_site(request)
    return HttpResponse(f"user is {request.user.username} and email is {request.user.email or 'not provided'} and site is {site.domain}")


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
        request.session['username'] = username
        if user is not None:
            login(request, user)
            return HttpResponse(f"Logged in as {user.username}")
        return HttpResponse("Invalid credentials")
    return HttpResponse("Send POST request to login")


@login_required
def logout_view(request):
    logout(request)
    request.session.flush()
    return HttpResponse("Logged out successfully")


@login_required
def dashboard(request):
    return HttpResponse(f"Welcome {request.user.username}")


def cokkie(req):
    response = HttpResponse("Cookie set")
    response.set_cookie('username', 'skipper', max_age=3600,
                        httponly=True, samesite='strict')
    return response


def get_cookie(req):
    cookie_value = req.COOKIES.get(
        'username', 'No cookie found')
    res = HttpResponse(f"Cookie value: {cookie_value}")
    res.delete_cookie('username')
    return res


def set_session(request):
    request.session['username'] = 'skippersession'
    request.session.set_expiry(0)
    return HttpResponse("Session set")


def get_session(request):
    username = request.session.get('username', 'No session found')
    request.session.flush()
    return HttpResponse(f"Session value: {username}")
    # flush means only 1 data is delete and clear will remove all data from session


def flush_session(request):
    request.session.flush()
    return HttpResponse("Session flushed")


logger = logging.getLogger(__name__)


# def log_test(request):
#     logger.debug("This is a debug message")
#     logger.info("This is an info message")
#     logger.warning("This is a warning message")
#     logger.error("This is an error message")
#     logger.critical("This is a critical message")
#     return HttpResponse("Logged some messages!")


@cache_page(60)
def cached_view(request):
    return HttpResponse(f'the item has been cached now')


def test_cache(request):
    # data = list(na.objects.all())
    # print(data)x
    cache.set("name", "skipper", timeout=60)
    # cache.set("list", data, timeout=60*2)
    value = cache.get("name")
    return HttpResponse(f"Value: {value}")


def test_caches(request):
    name = cache.get("name")
    return HttpResponse(f"Value from {name}")


def cache_demo(request, user_id):
    key = f"user:{user_id}"

    # SET
    cache.set("name", "Sai", timeout=60)

    # GET
    name = cache.get("name", "default_name")

    # ADD (only if not exists)
    cache.add("new_key", "only_once", timeout=60)

    # GET OR SET (with callable)
    user = cache.get_or_set(
        key,
        lambda: User.objects.get(id=user_id),
        timeout=300
    )

    # INCREMENT
    cache.set("counter", 1)
    cache.incr("counter")        # 2
    cache.incr("counter", 5)     # 7

    # DECREMENT
    cache.decr("counter")        # 6

    # TOUCH (extend expiry)
    cache.touch("name", timeout=120)

    # SET MANY
    cache.set_many({
        "a": 1,
        "b": 2,
        "c": 3
    }, timeout=60)

    # GET MANY
    values = cache.get_many(["a", "b", "c"])

    # DELETE
    cache.delete("new_key")

    # DELETE MANY
    cache.delete_many(["a", "b"])

    # CHECK EXISTENCE
    exists = cache.get("name") is not None

    # cache.clear()
    data = {
        "name": name,
        "user": user,
        "counter": cache.get("counter"),
        "bulk_values": values,
        "exists": exists
    }
    return HttpResponse(json.dumps(data, default=str), content_type="application/json")


def clear_cache(request):
    cache.clear()
    return HttpResponse("Cache cleared")


def send_custom_signal(request):
    custom_signal.send(sender=None, data="Hello from custom signal!")
    return HttpResponse("Custom signal sent!")


# def channel(req):
#     msg = req.GET.get("msg", "hello")
#     cache.set("channel:chat", msg, timeout=60)
#     return HttpResponse("channel layer view")


# def channel(request):
#     msg = request.GET.get("msg", "hello")
#     redis_client.publish("chat_channel", msg)

#     return JsonResponse({
#         "status": "sent",
#         "message": msg
#     })


# def receive_channel(request):
#     pubsub = redis_client.pubsub()
#     pubsub.subscribe("chat_channel")

#     print("Listening to chat_channel...")
#     # dont use .listen() in production as it will block the thread, use async or separate worker for listening to channel
#     # rather use .get_message() in a loop with sleep to check for new messages without blocking the thread
#     for message in pubsub.listen():
#         if message["type"] == "message":
#             print("Received:", message["data"])
#     return JsonResponse({
#         "status": "listening"})


def another_custom_signal_receiver(request):
    custom_signal.send_robust(
        sender="saikumar", data='hey', action='custom signal here')
    return HttpResponse("Another custom signal sent!")


def DB_sync_async(req):
    # user = await User.objects.aget(id=1)
    # user = await User.objects.afirst()
    # user = await User.objects.alast()
    # exists = await User.objects.filter(name="Sai").aexists()
    # users = await sync_to_async(list)(User.objects.all())
    # count = await User.objects.acount()
    # user = await User.objects.acreate(name="Sai")
    # await User.objects.filter(id=1).aupdate(name="New Name")
    # await User.objects.filter(id=1).adelete()
    # async for user in User.objects.all():
    #     print(user.name)
    # result = await User.objects.aaggregate(total=Count("id"))
    # obj, created = await User.objects.aget_or_create(name="Sai")
    # #realted objects
    # user = await User.objects.aget(id=1)
    # posts = await sync_to_async(list)(user.posts.all())
    return HttpResponse("DB operations done asynchronously!")


def conditions(req, *args, **kwargs):
    return "v2"


@condition(etag_func=conditions,  last_modified_func=None)
def conditional_view(req, *args, **kwargs):
    return HttpResponse("This is a conditional view")


signer = Signer()


def register(request):
    user_id = 5  # assume user created

    # create signed token
    token = signer.sign(str(user_id))

    # create verification link
    verify_url = request.build_absolute_uri(
        reverse('verify_email') + f'?token={token}'
    )

    print("Verification link:", verify_url)

    return HttpResponse(f"User registered! Check console for link.")


def verify_email(request):
    token = request.GET.get('token')

    try:
        # verify token
        user_id = signer.unsign(token)
        # activate user (fake logic)
        return HttpResponse(f"User {user_id} verified successfully ✅")
    except BadSignature:
        return HttpResponse("Invalid or tampered link ❌")


def user_update(request, id):
    if request.method == "PUT":
        try:
            data = json.loads(request.body.decode("utf-8"))
        except:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        user = User.objects.filter(id=id).first()
        if not user:
            return JsonResponse({"error": "User not found"}, status=404)
        allowed_fields = ["username", "email", "age"]
        updated_fields = {}
        for field, value in data.items():
            if field in allowed_fields:
                setattr(user, field, value)
                updated_fields[field] = value
        user.save()
        return JsonResponse({
            "message": "User updated successfully",
            "updated_data": updated_fields
        })


def user_get_dynamic(request, id):
    user = User.objects.filter(id=id).first()
    if not user:
        return JsonResponse({"error": "Not found"}, status=404)
    data = json.loads(request.body.decode("utf-8"))
    response = {}
    for field in data.keys():
        if hasattr(user, field):
            response[field] = getattr(user, field)
    return JsonResponse(response)


def names(req):
    d = data.objects.get(id=1)
    json_string = '{"name": "Alice", "age": 30, "is_student": false}'
    datas = json.loads(json_string)
    p = datas.get("fields", [])
    print(p)
    return HttpResponse(d.name)


# Request → as_view() → dispatch() → get()/post()
class dispatch(View):
    def dispatch(self, request, *args, **kwargs):
        print("Before dispatch")
        if not request.user.is_authenticated:
            response = HttpResponse("Unauthorized")
        response = super().dispatch(request, *args, **kwargs)
        print("After dispatch")
        return response

    def get(self, request):
        print("Inside GET method")
        return HttpResponse("GET response")

    # def post(self, request):
    #     return HttpResponse("POST response")


class dispatchtest(dispatch):
    def get(self, request):
        print("Inside GET method of dispatchtest")
        return HttpResponse("GET response from dispatchtest")


class AuthMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse("Unauthorized")

        print("AuthMixin before dispatch")
        response = super().dispatch(request, *args, **kwargs)
        print(response)
        print(response.content)
        print("AuthMixin after dispatch")
        return response


class DashboardView(AuthMixin, View):
    def get(self, request, *args, **kwargs):
        print("Inside GET")
        return HttpResponse("Dashboard")


@method_decorator(csrf_exempt, name='dispatch')
class MyView(View):
    def get(self, request):
        # super().dispatch(request)
        return HttpResponse("This is a GET request")

    def post(self, request):
        return HttpResponse("This is a POST request")

    def put(self, request):
        return HttpResponse("This is PUT request")

    def patch(self, request):
        return HttpResponse("This is a PATCH request")

    def delete(self, request):
        return HttpResponse("This is a DELETE request")


class loginmixin(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'n1.view_na'
# class loginmixin(LoginRequiredMixin,  View):
#     permission_required = 'n1.view_na'

    def get(self, request):
        return HttpResponse("This is a GET request for authenticated users only")


class JSONResponseMixin:
    def render_json(self, data):
        return JsonResponse(data)


class MyAPI(JSONResponseMixin, View):
    def get(self, request):
        return self.render_json({"msg": "Hello"})

# dispatch,get,post,query_set(),get_context_data(),form_valid(),form_invalid(),get_object(),get_queryset(),get_serializer(),get_serializer_class(),perform_create(),perform_update(),perform_destroy()


class UserListView(ListView):
    model = book
    template_name = 'n1/user_list.html'
    context_object_name = 'users'


# class detailview(DetailView):
#     model = book
#     template_name = 'n1/user_detail.html'
#     context_object_name = 'user'
#     pk_url_kwarg = 'id'


# class createview(CreateView):
#     model = book
#     fields = ['name', 'author']
#     template_name = 'n1/user_create.html'
#     success_url = '/n1/list/'


class listview(ListView):
    model = na
    queryset = na.objects.all()
    template_name = 'n1/book_list.html'
    content_type = 'application/json'
    context_object_name = 'users'
    paginate_by = 1000
    paginate_orphans = 1
    # paginator_class = Paginator
    # by default it gaves 5 limit

    def get_queryset(self):
        return na.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['extra_data'] = 'This is some extra data'
        return context

    def render_to_response(self, context, **response_kwargs):
        print("Rendering template...")
        return super().render_to_response(context, **response_kwargs)

    def get_paginate_by(self, queryset):
        try:
            limit = int(self.request.GET.get('limit', 5))
        except ValueError:
            limit = 5
        return min(limit, 1000)


class detailview(DetailView):
    model = book
    context_object_name = 'objectsss'
    pk_url_kwarg = 'id'
    # int_field = 'id'


# class ProductDetailView(DetailView):
#     model = book
#     slug_field = "slug"
#     slug_url_kwarg = "slug"

#     def get_object(self):
#         obj = super().get_object()
#         print(obj.name)
#         return obj

class ProductCreateView(CreateView):
    model = book
    # fields = ['name', 'price', 'description']
    fields = ['name', 'author']
    # template_name = "product_form.html"
    success_url = "/n1/mylist/"

    def dispatch(self, request, *args, **kwargs):
        print("CreateView called")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        print("Form is valid")
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Form errors:", form.errors)
        return super().form_invalid(form)


class ProductUpdateView(UpdateView):
    model = book
    # fields = ['name', 'price', 'description']
    fields = ['name', 'author']
    # template_name = "product_form.html"
    success_url = "/n1/mylist/"

    def dispatch(self, request, *args, **kwargs):
        print("UpdateView called")
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(book, pk=self.kwargs['pk'])

    def form_valid(self, form):
        print("Form valid - updating")
        return super().form_valid(form)


class deletebook(DeleteView):
    model = book
    template_name = "n1/book_delete.html"
    success_url = "/n1/mylist/"

    def dispatch(self, request, *args, **kwargs):
        print("DeleteView called")
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        res = get_object_or_404(book, pk=self.kwargs['pk'])
        print(f"Deleting book: {res}")
        return res


def pagination(req):
    data = list(na.objects.all().values())
    try:
        page_number = req.GET.get('page', 1)
    except (ValueError, TypeError):
        page_number = 1
    try:
        limit = int(req.GET.get('limit', 10))
    except (ValueError, TypeError):
        limit = 100

    limit = min(limit, 100)  # enforce max limit of 100

    paginator = Paginator(data, limit, orphans=5)

    page_obj = paginator.get_page(page_number)

    return JsonResponse({
        "page": page_obj.number,
        'next': page_obj.next_page_number() if page_obj.has_next() else None,
        'previous': page_obj.previous_page_number() if page_obj.has_previous() else None,
        "total_pages": paginator.num_pages,
        "len_data": len(list(page_obj)),
        "data": list(page_obj),
    })
# if page_obj.has_next():
#     next_page_url = f"?page={page_obj.next_page_number()}&limit={limit}"
# else:
#     next_page_url = None


class pages(View):
    def get(self, request):
        queryset = na.objects.all().order_by('id').values()
        try:
            page_number = int(request.GET.get('page', 1))
        except ValueError:
            page_number = 1
        try:
            limit = int(request.GET.get('limit', 10))
        except ValueError:
            limit = 10
        limit = min(limit, 100)
        paginator = Paginator(queryset, limit)
        page_obj = paginator.get_page(page_number)
        return JsonResponse({
            "page": page_obj.number,
            "total_page": page_obj.paginator.num_pages,
            "limit": limit,
            "total_pages": paginator.num_pages,
            "total_items": paginator.count,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
            "data": list(page_obj)
        })


def serlizer(req):
    # data = list(na.objects.all().values()[:50])
    serialized_data = serialize('json', na.objects.all()[:50])
    # print(serialized_data)
    return HttpResponse(serialized_data, content_type='application/json')


class DRFAPI(APIView):
    def get(self, request, id=None):
        if id is not None:
            queryset = na.objects.filter(id=id)
        else:
            queryset = na.objects.all()[:50]
        serializer = naSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, id=None):
        data = json.loads(request.body)
        serializer = naSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request, id):
        data = json.loads(request.body)
        instance = get_object_or_404(na, id=id)
        serializer = naSerializer(instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id):
        instance = get_object_or_404(na, id=id)
        instance.delete()
        return Response({"message": "Deleted successfully"})


class MyAPI(
    GenericAPIView,
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin
):
    queryset = na.objects.all()[:100]
    serializer_class = naSerializer
    lookup_field = "id"
    # obj = self.get_object() #only works with id

    # def get_serializer_class(self):
    #     if self.request.method == "GET":
    #         return UserReadSerializer
    #     return UserWriteSerializer
    #  obj = self.get_object()
    # serializer = self.get_serializer(obj) #if multiple then many=True
    # return Response(serializer.data)

    # serializer = self.get_serializer(obj, data=request.data, partial=True) #patch
    # serializer = self.get_serializer(obj, data=request.data) #put

    # GET → list OR retrieve

    def get(self, request, *args, **kwargs):
        if kwargs.get("id"):
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    # POST → create
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    # PUT → full update
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    # PATCH → partial update
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    # DELETE → delete
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

# Hooks:special places where you can add your own logic during create/update/delete
    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

    # def perform_update(self, serializer):
    #     serializer.save(updated_by=self.request.user)

    # def perform_destroy(self, instance):
    #     instance.delete()


class listcrete(ListCreateAPIView):
    queryset = na.objects.all().order_by('-id')[:100]
    serializer_class = naSerializer


class listonly(ListAPIView):
    queryset = na.objects.all().order_by('-id')[:50]
    serializer_class = naSerializer


class createonly(CreateAPIView):
    queryset = na.objects.all()
    serializer_class = naSerializer


class updateonly(UpdateAPIView):
    queryset = na.objects.all()
    serializer_class = naSerializer


class deleteonly(DestroyAPIView):
    queryset = na.objects.all()
    serializer_class = naSerializer


class multiple(RetrieveUpdateDestroyAPIView):
    queryset = na.objects.all()
    serializer_class = naSerializer
    lookup_field = "id"


class readonly(RetrieveAPIView):
    queryset = na.objects.all()
    serializer_class = naSerializer


class UserViewSet(ModelViewSet):
    # queryset = na.objects.all().order_by('-id')[:100]
    # queryset = na.objects.all().order_by('-id')
    # in modelviewset we should not give slice in queryset because it will be used for all operations like retrieve, update, delete etc and it will cause error if we try to retrieve or update an object that is not in the sliced queryset
    # get_object_or_404 will not work if we give slice in queryset because it will try to get object from sliced queryset and if object is not in sliced queryset then it will return 404 error even if object exists in database(get_object_or_404(queryset, id=27531))
    serializer_class = naSerializer

    def get_queryset(self):
        qs = na.objects.all().order_by('-id')
        print(self.action)
        if self.action == "list":
            return qs[:10]
        return qs

    # def get_object(self):
    #     return get_object_or_404(self.get_queryset(), id=self.kwargs['id'],user=self.request.user)

# .actions → which operation is being performed now!
# @action(detail=False, methods=['get']),deatil means specifc id

    @action(detail=True, methods=['post'])
    def changename(self, request, pk=None):
        user = self.get_object()
        print(user)
        user.name = 'lastbaba'
        user.save()
        return Response({"message": f"User {user.id} changed the name "})

    def destroy(self, request, *args, **kwargs):
        return Response({"message": "Delete is not allowed"}, status=403)

    def update(self, request, *args, **kwargs):
        raise PermissionDenied("Update not allowed")

    def partial_update(self, request, *args, **kwargs):
        raise PermissionDenied("Partial update not allowed")

    def create(self, request, *args, **kwargs):
        raise PermissionDenied("Create not allowed")

    def list(self, request, *args, **kwargs):
        raise PermissionDenied("Listing not allowed")

    # def retrieve(self, request, *args, **kwargs):
    #     raise PermissionDenied("Listing not allowed")


class viewset(ViewSet):
    def list(self, req):
        user = na.objects.all().order_by('-id')[:10]
        serializer = naSerializer(user, many=True)
        return Response(serializer.data)

    def create(self, req):
        serlizer = naSerializer(data=req.data)
        if serlizer.is_valid():
            serlizer.save()
            return Response(serlizer.data, status=201)
        return Response(serlizer.errors, status=400)

    def retrieve(self, req, pk=None):
        user = get_object_or_404(na, pk=pk)
        serializer = naSerializer(user)
        return Response(serializer.data)

    def update(self, req, pk=None):
        user = get_object_or_404(na, pk=pk)
        serializer = naSerializer(user, data=req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def partial_update(self, req, pk=None):
        user = get_object_or_404(na, pk=pk)
        serializer = naSerializer(user, data=req.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, req, pk=None):
        user = get_object_or_404(na, pk=pk)
        user.delete()
        return Response({"message": "Deleted successfully"})


class readonlyviewset(ReadOnlyModelViewSet):
    serializer_class = naSerializer

    def get_queryset(self):
        qs = na.objects.all().order_by('-id')
        if self.action == "list":
            return qs[:10]
        return qs


@api_view(['GET'])
def bookdaata(req):
    # books = list(book.objects.get(id=1))
    books = book.objects.all()
    serlizer = booksSerializer(books, many=True)
    # return JsonResponse(serlizer.data, safe=False)
    return Response(serlizer.data)


class bookhyperlink(ModelViewSet):
    queryset = user.objects.all()
    serializer_class = BookSerializer
    # lookup_field = 'id'
    # lookup_url_kwarg = 'id'


@api_view(['GET'])
def authorlist(req):
    author_a = autor.objects.all()
    serlizer = authorsSerializer(author_a, many=True)
    return Response(serlizer.data)


@csrf_exempt
@api_view(['POST', 'GET'])
def create_book(req):
    # data = json.loads(req.body)
    serlizer = booksSerializer(data=req.data)
    if serlizer.is_valid():
        serlizer.save()
        return Response(serlizer.data, status=201)
    return Response(serlizer.errors, status=400)


class justcheck(APIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get(self, request):
        return Response({"message": "This is a throttled view"})


class customthrottle(APIView):
    # throttle_classes = [notloggedinthrottle, loginthrottle]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "booksthrottle"

    def get(self, request):
        return Response({"message": "This view is for custom throttle testing"})


# class filter(ModelViewSet):
#     queryset = user.objects.all()
#     serializer_class = userSerializer
#     filterset_fields = ['name', 'id']


class filter(ModelViewSet):
    queryset = na.objects.all().order_by('-id')
    serializer_class = naSerializer
    filterset_fields = ['name', 'id']
    pagination_class = CustomPagination


class limitpagintion(ListAPIView):
    queryset = na.objects.all()
    serializer_class = naSerializer
    pagination_class = CursorPagination


class customfilter(ModelViewSet):
    queryset = user.objects.all()
    serializer_class = userSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'id']
    # filterset_fields = ['price__gt', 'price__lt', 'name__icontains','price':['gt']]
    search_fields = ['name']
    ordering_fields = ['id', 'name']
# /customfilter/?ordering=name
# /customfilter/?search=is
# /customfilter/?name=jason


# serializer = BookSerializer(queryset, many=True, context={'request': request}) ^^^^^^^^^^^^^^^^^^^^^^^^^
# AttributeError: type object 'limitpagination' has no attribute 'get_extra_actions'
