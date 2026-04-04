from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Prints hello message"

    def add_arguments(self, parser):
        parser.add_argument("name", type=str)
        parser.add_argument("-age", type=int)
        parser.add_argument("-war", type=str)

    def handle(self, *args, **kwargs):
        name = kwargs['name']
        age = kwargs['age']
        war = kwargs['war']
        self.stdout.write("Hello man! Django custom command working!")
        self.stdout.write(self.style.SUCCESS(
            f"Your name is {name}, your age is {age}, and your war is {war}"))
        self.stdout.write(self.style.WARNING(
            f"This is a warning message and {war}"))
        self.stdout.write(self.style.ERROR("This is an error message"))
