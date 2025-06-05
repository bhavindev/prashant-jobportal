from apps.settings.models import *
from apps.authapp.models import UserProfile
from apps.userapp.models import supportTicket
from apps.homepage.models import projectsSection, serviceSection
from django.conf import settings
from apps.hrm.models import Notification
from django.db.models import Q
from django.utils import timezone
from apps.lang.models import Languages

## Settings Context Proccessor
def website_settings_context(request):
    # Get the default language
    default_language = Languages.objects.filter(is_default=True).first()
    
    # Get the selected language from session or use default language
    selected_language_code = request.session.get('selected_language', default_language.code)
    
    settings = websiteSetting.objects.filter(language__code=selected_language_code).first()
    
    return {'settings': settings}

def seo_settings_context(request):
    # Get the default language
    default_language = Languages.objects.filter(is_default=True).first()
    
    # Get the selected language from session or use default language
    selected_language_code = request.session.get('selected_language', default_language.code)
    
    seo_settings = SeoSetting.objects.filter(language__code=selected_language_code).first()
    
    return {'seo_settings': seo_settings}

def menu_context(request):
    # Get the default language
    default_language = Languages.objects.filter(is_default=True).first()
    
    # Get the selected language from session or use default language
    selected_language_code = request.session.get('selected_language', default_language.code)
    
    menus = Menu.objects.filter(language__code=selected_language_code).order_by('order')
    
    return {'menus': menus}

def header_footer_context(request):
    # Get the default language
    default_language = Languages.objects.filter(is_default=True).first()
    
    # Get the selected language from session or use default language
    selected_language_code = request.session.get('selected_language', default_language.code)
    
    header_footer = HeaderFooter.objects.filter(language__code=selected_language_code).first()
    
    return {'header_footer': header_footer}

## User Profile Context Proccessor
def user_profile_context(request):
    user_profile = None
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.filter(user=request.user).first()
    return {
        'user_profile': user_profile
    }

## Project Context Proccessor
def project_context(request):
    # Get the default language
    default_language = Languages.objects.filter(is_default=True).first()
    
    # Get the selected language from session or use default language
    selected_language_code = request.session.get('selected_language', default_language.code)
    
    projects = projectsSection.objects.filter(language__code=selected_language_code).order_by('-title')
    
    return {'global_projects' : projects}

## Service Context Proccessor
def service_context(request):
    # Get the default language
    default_language = Languages.objects.filter(is_default=True).first()
    
    # Get the selected language from session or use default language
    selected_language_code = request.session.get('selected_language', default_language.code)
    
    services = serviceSection.objects.filter(language__code=selected_language_code).order_by('-title')
    
    return {'global_services' : services}

## Ticket Context Proccessor
def unsolved_tickets_context(request):
    opened_ticket = supportTicket.objects.filter(status='open')
    return {'opened_ticket' : opened_ticket}


## Demo Mode Template Context Proccessor
def demo_mode_enabled(request):
    return {'demo_mode_enabled': 'core.middleware.middleware.DemoModeMiddleware' in settings.MIDDLEWARE}

## Notification Context Proccessor
def notification_context(request):
    if request.user.is_authenticated:
        if request.user.role == 'admin':
            notifications = Notification.objects.all().order_by('-created_at')
        elif request.user.role == 'Manager' or request.user.role == 'HR':
            notifications = Notification.objects.filter(
                branch=request.user.userprofile.branch).order_by('-created_at')
        else:
            notifications = Notification.objects.filter(
                branch=request.user.userprofile.branch ).order_by('-created_at')
        
        unread_notification_count = Notification.objects.exclude(Q(readed_by=request.user)).count()
    
        return {'notifications': notifications, 'notification_count': unread_notification_count}
    else:
        return {'notifications': None, 'notification_count': 0}
    
## Language Context Proccessor
def language_context(request):
    default_language = Languages.objects.filter(is_default=True).first()
    selected_language_code = request.session.get('selected_language', default_language.code)
    selected_language = Languages.objects.filter(code=selected_language_code).first()
    languages = Languages.objects.all()
    return {
        'selected_language_code': selected_language_code,
        'selected_language': selected_language,
        'languages': languages
    }
    
## Promo Banner Context Proccessor
def promo_banner_context(request):
    # Get the default language
    default_language = Languages.objects.filter(is_default=True).first()
    
    # Get the selected language from session or use default language
    selected_language_code = request.session.get('selected_language', default_language.code)
    
    promo_banner = PromotionalBanner.objects.filter(language__code=selected_language_code).first()
    
    is_date_over = True
    if promo_banner:
        if promo_banner.promo_end_date:
            # Ensure the banner is active for the entire last day
            if promo_banner.promo_end_date >= timezone.now().date():
                is_date_over = False
    
    return {'promo_banner': promo_banner, 'is_promo_date_over': is_date_over}
