from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig

#for custom admin site we need to create a class inheriting AdminConfig and then we need to set default_site to our custom admin site and then we need to add this class in our settings.py file in INSTALLED_APPS instead of django.contrib.admin

# class another(AdminConfig):
#     default_site = 'n1.admin.AnotherAdminSite'

class N1Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'n1'
