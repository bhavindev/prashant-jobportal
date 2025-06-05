from django.apps import AppConfig
from django.conf import settings


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.blog'

    def ready(self):
        import apps.blog.signals
        
        if getattr(settings, 'ENABLE_BANGLA_SIGNALS', False):
            import apps.blog.bangla_signals
            
        if getattr(settings, 'ENABLE_ARABIC_SIGNALS', False):
            import apps.blog.arabic_signals