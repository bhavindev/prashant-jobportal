from django_user_agents.utils import get_user_agent
import requests
from apps.analytics.models import *
from django.db.models import Count, Sum

def get_user_os(request):
    user_agent = get_user_agent(request)
    print('OS is: ',user_agent.os.family)

    if user_agent.is_bot:
        return 'Others'
    else:
        return user_agent.os.family 

def get_user_browser(request):
    user_agent = get_user_agent(request)
    print('Browser is: ',user_agent.browser.family)

    if user_agent.is_bot:
        return 'Others'
    else:
        return user_agent.browser.family

def get_user_device(request):
    user_agent = get_user_agent(request)
    print('Device is: ',user_agent.device.family)

    if user_agent.is_bot:
        return 'Others'
    else:
        return user_agent.device.family
    
def visitor_data(request):
    user_browser = get_user_browser(request)
    user_os = get_user_os(request)
    user_device = get_user_device(request)

    if 'visited' not in request.session:
        Visitor.objects.create(
            count=1,
            os=user_os,
            browser=user_browser,
            device=user_device,
        )
        request.session['visited'] = True
        
def format_visitor_count(count):
    if count < 1000:
        return str(count)
    elif count < 1_000_000:
        formatted_count = f"{count/1000:.2f}"
        return formatted_count.rstrip('0').rstrip('.') + 'k'
    elif count < 1_000_000_000:
        formatted_count = f"{count/1_000_000:.2f}"
        return formatted_count.rstrip('0').rstrip('.') + 'M'
    else:
        formatted_count = f"{count/1_000_000_000:.2f}"
        return formatted_count.rstrip('0').rstrip('.') + 'B'

def analyticsData(request):
    total_visitors = Visitor.objects.aggregate(Sum('count'))['count__sum'] or 0
    formatted_total_visitors = format_visitor_count(total_visitors)

    os_counts = Visitor.objects.values('os').annotate(count=Count('os')).order_by('-count')
    browser_counts = Visitor.objects.values('browser').annotate(count=Count('browser')).order_by('-count')
    device_counts = Visitor.objects.values('device').annotate(count=Count('device')).order_by('-count')

    total_os = sum(entry['count'] for entry in os_counts)
    total_browser = sum(entry['count'] for entry in browser_counts)
    total_device = sum(entry['count'] for entry in device_counts)

    os_percentages = [
        {'name': entry['os'], 'percentage': round((entry['count'] / total_os) * 100)} if total_os != 0
        else {'name': entry['os'], 'percentage': 0}
        for entry in os_counts
    ]
    device_percentages = [
        {'name': entry['device'], 'percentage': round((entry['count'] / total_device) * 100)} if total_device != 0
        else {'name': entry['device'], 'percentage': 0}
        for entry in device_counts
    ]
    browser_percentages = [
        {'name': entry['browser'], 'percentage': round((entry['count'] / total_browser) * 100)} if total_browser != 0
        else {'name': entry['browser'], 'percentage': 0}
        for entry in browser_counts
    ]

    return {
        'total_visitors': formatted_total_visitors,
        'os_percentages': os_percentages,
        'browser_percentages': browser_percentages,
        'device_percentages': device_percentages,
    }