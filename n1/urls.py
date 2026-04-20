from django.urls import path, register_converter
from n1.url_converter import four_int, uuids

from n1.views import *

register_converter(four_int, 'f')
register_converter(uuids, 'u')

app_name = "n1"

urlpatterns = [
    path('a/', hello),
    path('data/', names),
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
    path('channel/', channel),
    path('receive-channel/', receive_channel),
    path('cache-demo/<int:user_id>/', cache_demo, name='all cache names'),
    path('clear-cache/', clear_cache),
    path('custom-signal/', send_custom_signal),
    path('another-custom-signal/', another_custom_signal_receiver),
    path('conditional-view/', conditional_view),
    path('register/', register, name='register'),
    path('verify/', verify_email, name='verify_email'),
    path('myviewclass/', MyView.as_view(), name='my_view_class'),
    path('list/', UserListView.as_view(), name='user_list'),
    path('dispatch/', dispatch.as_view(), name='dispatch_view'),
    path('dispatchtest/', dispatchtest.as_view(), name='dispatch_test_view'),
    path('dashboard1/', DashboardView.as_view(), name='dashboard'),
    path('loginmixin/', loginmixin.as_view(), name='login_mixin'),
    path('mylist/', listview.as_view(), name='my_list'),
    path('list/<int:id>/', detailview.as_view(), name='user_detail'),
    path('lists/<int:pk>/', detailview.as_view(), name='user_detail'),
    # path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail')
    path('createbook/', ProductCreateView.as_view(), name='create_book'),
    path('updatebook/<int:pk>/', ProductUpdateView.as_view(), name='update_book'),
    path('deletebook/<int:pk>/', deletebook.as_view(), name='delete_book'),

]
