from django.contrib import admin

from .models import *


@admin.register(usser)
class usserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city')
    search_fields = ('name', 'status')
    ordering = ('id',)


@admin.register(post)
class postAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'status', 'views', 'author')
    list_filter = ('status', 'views')
    search_fields = ('title', 'content')
    ordering = ('id',)


@admin.register(na)
class naAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created', 'updated', )
    list_filter = ('created', 'updated')
    search_fields = ('name',)
    ordering = ('id',)


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


@admin.register(com2)
class com2Admin(admin.ModelAdmin):
    list_display = ('id', 'name', 'age')
    search_fields = ('name',)


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
