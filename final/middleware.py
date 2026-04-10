# class middleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         print("Before view")
#         response = self.get_response(request)
#         print("After view")
#         return response
from django.core.cache import cache


class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def process_view(self, request, view_func, view_args, view_kwargs):
        match = request.resolver_match
        if match and match.app_name == "n2":
            raise Exception("Blocked n2 app 🚫")
        print(f"Processing view: {view_func.__name__}")

    def process_exception(self, request, exception):
        from django.http import JsonResponse
        return JsonResponse({"error": str(exception)}, status=500)

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        key = f"rate:{ip}"

        requests = cache.get(key, 0)

        if requests > 20:
            from django.http import HttpResponse
            return HttpResponse("Too many requests", status=429)

        cache.set(key, requests + 1, timeout=60)

        if request.path.startswith("/admin/"):
            # if 'admin' in request.path:
            return self.get_response(request)
            # raise Exception("Admin access is not allowed man!")

        if "skipper" in request.path:
            raise Exception("Invalid query parameter")

        return self.get_response(request)
