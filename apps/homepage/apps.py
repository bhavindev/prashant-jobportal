from django.apps import AppConfig
from django.conf import settings


class HomepageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.homepage'
    
    def ready(self):
        import apps.homepage.signals
        
        if getattr(settings, 'ENABLE_BANGLA_SIGNALS', False):
            import apps.homepage.bangla_signals
        
        if getattr(settings, 'ENABLE_ARABIC_SIGNALS', False):
            import apps.homepage.arabic_signals
            
        
