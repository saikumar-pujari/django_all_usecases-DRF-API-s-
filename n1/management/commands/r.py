from django.core.management.base import BaseCommand, CommandParser
from django.core.management import call_command


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("port", type=int, default=8000, nargs="?")

    def handle(self, *args, **kwargs):
        port = kwargs['port']
        call_command("runserver_plus", f"localhost:{port}")
