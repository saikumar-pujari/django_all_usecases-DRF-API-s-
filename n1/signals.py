from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.core.signals import request_finished, request_started
from django.dispatch import receiver, Signal

User = get_user_model()

custom_signal = Signal()


@receiver(user_logged_in, sender=User)
def login_succes(sender, request, user, **kwargs):
    print("Login successful for user:", user.username)


@receiver(user_logged_out, sender=User)
def logout_succes(sender, request, user, **kwargs):
    print("Logout successful for user:", user.username)


# @receiver(request_finished)
# def request_finished_signal(sender, **kwargs):
#     print("Request finished signal received.")


# @receiver(request_started)
# def request_started_signal(sender, **kwargs):
    # print(sender)
    # print(kwargs)
    # print("Request started signal received.")

    # there are many more signals available in django, you can check the documentation for more details.
    # like pre_init,post_init,pre_save, post_save, pre_delete, post_delete, pre_migrate, post_migrate,at_ending_request,request_finished. You can use these signals to perform actions before or after certain events occur in your application.


@receiver(custom_signal)
def custom_signal_receiver(sender, **kwargs):
    print("Custom signal received with data:", kwargs)
