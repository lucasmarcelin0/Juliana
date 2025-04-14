from django.apps import AppConfig

class SalesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sales'

    def ready(self):
        import sales.signals  # <-- Isso ativa o sinal automaticamente quando a app é carregada
