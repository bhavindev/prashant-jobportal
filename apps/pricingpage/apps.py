from django.apps import AppConfig
from django.conf import settings


class PricingpageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.pricingpage'
    
    def ready(self):
        import apps.pricingpage.signals
        
        if getattr(settings, 'ENABLE_BANGLA_SIGNALS', False):
            import apps.pricingpage.bangla_signals
        
        if getattr(settings, 'ENABLE_ARABIC_SIGNALS', False):
            import apps.pricingpage.arabic_signals
