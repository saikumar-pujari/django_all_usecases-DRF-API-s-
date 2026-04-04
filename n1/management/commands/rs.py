from django.core.management.base import BaseCommand
import subprocess
import time
import sys


class Command(BaseCommand):
    help = "Run Django server with full retry (even on syntax errors)"

    def add_arguments(self, parser):
        parser.add_argument("--delay", type=int, default=2)
        parser.add_argument("--retries", type=int, default=5)

    def handle(self, *args, **options):
        delay = options["delay"]
        retries = options["retries"]

        attempt = 0

        while retries == 0 or attempt < retries:
            attempt += 1

            self.stdout.write(f"\n🚀 Starting server (Attempt {attempt})...\n")

            try:
                process = subprocess.run(
                    [sys.executable, "manage.py", "runserver"],
                )

                self.stdout.write(self.style.ERROR("💥 Server stopped/crashed"))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error: {e}"))

            self.stdout.write(f"⏳ Retrying in {delay} seconds...\n")
            time.sleep(delay)

        self.stdout.write(self.style.WARNING("❌ Max retries reached"))
