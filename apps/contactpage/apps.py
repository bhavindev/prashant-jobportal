from django.apps import AppConfig
from django.conf import settings

class ContactpageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.contactpage'

    def ready(self):
        import apps.contactpage.signals
        
        if getattr(settings, 'ENABLE_BANGLA_SIGNALS', False):
            import apps.contactpage.bangla_signals
            
        if getattr(settings, 'ENABLE_ARABIC_SIGNALS', False):
            import apps.contactpage.arabic_signals