from django.urls import path, register_converter
from n1.url_converter import four_int, uuids

from n1.views import *

register_converter(four_int, 'f')
register_converter(uuids, 'u')

app_name = "n1"

urlpatterns = [
    path('a/', hello),
    path('skipper/', hello),
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
    path("set-cookie/", cokkie),
    path("get-cookie/", get_cookie),
    path("set-session/", set_session),
    path("get-session/", get_session),
    path("flush-session/", flush_session),
    # path("log-test/", log_test),
    path("cached/", cached_view),
    path("test-cache/", test_cache),
    path("test-caches/", test_caches),
    path('cache-demo/<int:user_id>/', cache_demo),
    path('clear-cache/', clear_cache),
    path('custom-signal/', send_custom_signal),
    path('another-custom-signal/', another_custom_signal_receiver),
    path('conditional-view/', conditional_view),
]
