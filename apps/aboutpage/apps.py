from django.apps import AppConfig
from django.conf import settings


class AboutpageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.aboutpage'
    
    def ready(self):
        import apps.aboutpage.signals
        
        if getattr(settings, 'ENABLE_BANGLA_SIGNALS', False):
            import apps.aboutpage.bangla_signals
        
        if getattr(settings, 'ENABLE_ARABIC_SIGNALS', False):
            import apps.aboutpage.arabic_signals