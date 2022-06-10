# from django.apps import AppConfig


# class AccountsConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'accounts'

#     def ready(self) -> None:
#         import accounts.signals
#         return super().ready()

from django.apps import AppConfig
from django.db.models.signals import post_migrate


class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        from .signals import populate_models
        post_migrate.connect(populate_models, sender=self)