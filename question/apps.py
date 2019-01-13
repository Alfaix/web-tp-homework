from django.apps import AppConfig


class QuestionConfig(AppConfig):
    name = 'question'

    def ready(self):
        from question import signals
