from django.apps import AppConfig
from django.conf import settings


class PortfoliopageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.portfoliopage'
    
    def ready(self):
        import apps.portfoliopage.signals
        
        if getattr(settings, 'ENABLE_BANGLA_SIGNALS', False):
            import apps.portfoliopage.bangla_signals
            
        if getattr(settings, 'ENABLE_ARABIC_SIGNALS', False):
            import apps.portfoliopage.arabic_signals
