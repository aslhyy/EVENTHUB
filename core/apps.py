from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from decouple import config

class CoreConfig(AppConfig):
    name = "core"

    def ready(self):
        post_migrate.connect(create_superuser, sender=self)


def create_superuser(sender, **kwargs):
    User = get_user_model()

    username = config("DJANGO_SUPERUSER_USERNAME", default=None)
    email = config("DJANGO_SUPERUSER_EMAIL", default=None)
    password = config("DJANGO_SUPERUSER_PASSWORD", default=None)

    if not all([username, email, password]):
        return

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )
