from django.apps import AppConfig


class QuestsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "quests"

    def ready(self):
        from .views import start # <= さっき作った start関数をインポート
        start()