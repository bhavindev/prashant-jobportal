from django.apps import AppConfig
from django.conf import settings


class SettingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.settings'
    
    def ready(self):
        import apps.settings.signals
        
        if getattr(settings, 'ENABLE_BANGLA_SIGNALS', False):
            import apps.settings.bangla_signals
        
        if getattr(settings, 'ENABLE_ARABIC_SIGNALS', False):
            import apps.settings.arabic_signals
