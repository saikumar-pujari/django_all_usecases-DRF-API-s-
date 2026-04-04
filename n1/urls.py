from django.urls import path, register_converter
from n1.url_converter import four_int, uuids

from n1.views import *

register_converter(four_int, 'f')
register_converter(uuids, 'u')

urlpatterns = [
    path('a', hello),
    path('b/<str:name>/', nab),
    path('bb/<f:name>/', nab),
    path('c/<str:name>/<str:kw>/', nab),
    path('e/', n),
    path('1/', a),
    path('uuid/<uuid:uuid>/', uuid),
    path('uuids/<u:uuid>/', uuid),
    path("send-email/", send_email_view),
    path("get-name/", get_from_request),
    path("my-view/", my_view),
    path("post-view/", post_view),
    path("api-view/", api_view),
    path("all-view/", all_view),
    path("user-test/", user_test),
    path("register/", register_view),
    path("login/", login_view),
    path("logout/", logout_view),
    path("dashboard/", dashboard),

]
