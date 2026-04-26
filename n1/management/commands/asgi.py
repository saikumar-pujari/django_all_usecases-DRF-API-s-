import uvicorn
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        uvicorn.run("final.asgi:application",
                    host="127.0.0.1", port=8000, reload=True)


# we also can use daphne to run the server instead of using the default runserver command, which is based on WSGI. Daphne is an ASGI server that can handle asynchronous tasks and WebSockets, making it suitable for modern Django applications that require real-time features. To run the server with daphne, you can use the following command:
# daphne -p 8000 final.asgi:application
# and uvicorn as another ASGI server:
# uvicorn final.asgi:application --reload
