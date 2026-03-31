import os

from django.core.asgi import get_asgi_application
# from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'final.settings.dev')
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'final.settings')

# application = ASGIStaticFilesHandler(get_asgi_application())
application = get_asgi_application()


# environ:just a dict from sever(request) to application(response)
# {
#     'REQUEST_METHOD': 'GET',
#     'PATH_INFO': '/home/',
#     'QUERY_STRING': 'name=sai',
#     'HTTP_USER_AGENT': 'Chrome',
# }
# request(environ) = {
#     method: "GET",
#     path: "/home/",
#     GET: QueryDict,
#     POST: QueryDict,
#     FILES: MultiValueDict,
#     headers: dict,
#     body: bytes,
#     user: User,
#     session: Session,
# }

# next WSGIRequest creation using the get_asgi_application()
# class WSGIRequest(HttpRequest):
#     def __init__(self, environ):
#         self.environ = environ
#         self.method = environ['REQUEST_METHOD']
#         self.path = environ['PATH_INFO']
# after this django wraps it and gives us mainly(request.method, request.path), request.GET, request.POST, request.FILES, request.headers, request.body, request.user, request.session

# now query_is build first environ and then django wraps it
# from QUERY_STRING = "name=skipper&age=20"
# django request.get=QueryDict({'name': 'skipper', 'age': '20'}) #if file is there then request.FILES=MultiValueDict({'file': <InMemoryUploadedFile: file.txt (text/plain)>}) in memory stored them

# then it checks the header and authorization
# enviorn HTTP_USER_AGENT,HTTP_AUTHORIZATION
# django request.headers.get('User-Agent') #chrome
# django request.headers.get('Authorization') #Bearer token

# after this body,auth,session is build
# django request.body, request.user =user object, request.session,request.COOKIES
