from django.http import HttpResponse
from rest_framework.permissions import BasePermission, DjangoModelPermissions


class isloggedin(BasePermission):
    # has_permission before object is fetched
    def has_permission(self, request, view):
        # view gives us the view that is being accessed(modelviewset)
        # from this we can get the view.action,view.kwargs,view.queryset,view.serializer_class
        return request.user.is_authenticated
    # has_object_permission after object is fetched

    def has_object_permission(self, request, view, obj):
        # request incomming request
        # obj is the object that is being accessed(obj.id,obj.name)
        # return obj == request.user
        return obj.owner == request.user


class issuperuser(BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            # return request.user.is_authenticated
            return HttpResponse("You are not allowed to access this view.")
        return request.user.is_superuser
