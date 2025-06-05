from django.apps import AppConfig
from django.conf import settings


class ServicepageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.servicepage'
    
    def ready(self):
        import apps.servicepage.signals
        
        if getattr(settings, 'ENABLE_BANGLA_SIGNALS', False):
            import apps.servicepage.bangla_signals
            
        if getattr(settings, 'ENABLE_ARABIC_SIGNALS', False):
            import apps.servicepage.arabic_signals
