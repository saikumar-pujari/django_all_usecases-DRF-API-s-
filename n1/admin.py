from typing import Any
from urllib import request

import django.apps
from django.contrib import admin
from django.forms.models import ModelForm
from django.http import HttpRequest
from django.http.response import HttpResponse

from .models import *

admin.site.register(data)


@admin.register(usser)
class usserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city')
    search_fields = ('name', 'status')
    ordering = ('id',)


@admin.register(post)
class postAdmin(admin.ModelAdmin):
    raw_id_fields = ('author',)
    list_display = ('id', 'title', 'content', 'status', 'views', 'author')
    list_filter = ('status',)
    search_fields = ('title', 'content')
    ordering = ('id',)
    list_display_links = ('id', 'title')
    readonly_fields = ('views',)
    # the get_form method is used to customize the form that is used to create and edit objects in the admin interface. In this case, we are disabling the 'status' field for non-superusers, so that they cannot change the status of a post.
    # here the obj refers to creting or updateing an object if obj is None then it is creating an object otherwise it is updating an object

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        if not request.user.is_superuser:
            form.base_fields['status'].disabled = True
        if obj:
            print(f"Editing object: {obj}")
        else:
            print("Adding object")
            #  if obj:  # CHANGE(obj exists)
            #     kwargs['fields'] = ['name', 'status']
            # else:    # ADD(obj does not exist or creating an object)
            #     kwargs['fields'] = ['name']

        return form

    def get_object(self, request: HttpRequest, object_id: str, from_field: None = ...) -> Any | None:
        obj = super().get_object(request, object_id, from_field)
        if obj and not request.user.is_superuser:
            return obj
        # return print("You are not allowed to view this object")
        return None

    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs
    #     return qs.filter(user=request.user)

    def has_delete_permission(self, request: HttpRequest, obj: Any | None = ...) -> bool:
        return False

    def history_view(self, request, object_id, extra_context=None):

        # extra_context = extra_context or {}  # ✅ FIX

        # extra_context['msg'] = "Hello 🔥"

        return super().history_view(request, object_id, extra_context)

    # def is_published(self, obj):
    #     return obj.status == 'published'
    # is_published.boolean = True

    # actions = ['make_published']
    # def make_published(self, request, queryset):
    #     queryset.update(status='published')

# @admin.register(post)
# class postsAdmin(admin.ModelAdmin):
#     fieldsets = (
#         ('Basic Info', {
#             'fields': ('content')
#         }),
#         ('Meta Info', {
#             'fields': ('author', 'status'),
#             'classes': ('collapse',)
#         }),
#     )


@admin.register(na)
class naAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created', 'updated', )
    list_filter = ('created', 'updated')
    search_fields = ('name',)
    ordering = ('id',)
    list_per_page = 500


@admin.register(ba)
class baAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created', 'updated', )
    list_filter = ('created', 'updated')
    search_fields = ('name',)
    ordering = ('id',)


@admin.register(com1)
class com1Admin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city', 'pincode')
    search_fields = ('name',)
    list_editable = ('pincode',)


@admin.register(com2)
class com2Admin(admin.ModelAdmin):
    list_display = ('id', 'name', )
    search_fields = ('name',)
    exclude = ('age',)


@admin.register(autor)
class autorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(book)
class bookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author')
    search_fields = ('name',)
    ordering = ('id',)


@admin.register(user)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "user"]


@admin.register(ProfileProtect)
class ProfileProtectAdmin(admin.ModelAdmin):
    list_display = ["id", "user"]


@admin.register(ProfileNull)
class ProfileNullAdmin(admin.ModelAdmin):
    list_display = ["id", "user"]


@admin.register(ProfileDefault)
class ProfileDefaultAdmin(admin.ModelAdmin):
    list_display = ["id", "user"]


@admin.register(ProfileRestrict)
class ProfileRestrictAdmin(admin.ModelAdmin):
    list_display = ["id", "user"]


@admin.register(names)
class namesAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(namesproxy)
class namesproxyAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(uuidmodel)
class uuidmodelAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(uuidsmodel)
class uuidsmodelAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(images)
class imagesAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "images", "docu"]


class anotheradmin(admin.AdminSite):
    site_header = "another_admin_panel"
    site_title = "another_title_panel"
    index_title = "another_index_panel"


another = anotheradmin(name='anotheradmin')

# in main urls.py
# path('anotheradmin/', another.urls),
# another.register(post, postAdmin)
# another.register(model.post)

models = django.apps.apps.get_models()
# print(models)
for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
# admin.site.unregister(django.contrib.auth.models.Group)
# admin.site.unregister(django.contrib.auth.models.User)
# admin.site.unregister(django.contrib.sessions.models.Session)

# @admin.register(Post)
# class PostAdmin(admin.ModelAdmin):
#     list_display = ['title', 'author', 'status']
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         if request.user.is_superuser:
#             return qs
#         return qs.filter(author=request.user)
#     def save_model(self, request, obj, form, change):
#         if not obj.author:
#             obj.author = request.user
#         super().save_model(request, obj, form, change)
#     def has_change_permission(self, request, obj=None):
#         if obj and not request.user.is_superuser:
#             return obj.author == request.user
#         return True
#     def has_delete_permission(self, request, obj=None):
#         return request.user.is_superuser
#     def get_readonly_fields(self, request, obj=None):
#         if not request.user.is_superuser:
#             return ['status']
#         return []
