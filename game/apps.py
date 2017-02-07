from django.apps import AppConfig


class GameConfig(AppConfig):
    name = 'game'

    def ready(self):
        from game import signals
