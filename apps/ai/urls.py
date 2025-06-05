from django.urls import path 
from apps.ai.views import *

urlpatterns = [
    # For Admin
    path('admin/crm/ai-assistant/', aiCategory, name='aiCategory'),
    path('admin/crm/ai-assistant/history/', aiHistory, name='aiHistory'),
    path('admin/crm/ai-assistant/delete/<int:id>/', aiHistoryDelete, name='aiHistoryDelete'),
    path('ai-assistant/content-generator/category/<str:category>/', openAiContentGeneration, name='openAiContentGeneration'),
    
    # For User
    path('user/dashboard/ai-assistant/', useraiCategory, name='useraiCategory'),
    path('user/dashboard/ai-assistant/history/', useraiHistory, name='useraiHistory'),
    path('user/dashboard/ai-assistant/delete/<int:id>/', useraiHistoryDelete, name='useraiHistoryDelete'),
    path('user/ai-assistant/content-generator/category/<str:category>/', useropenAiContentGeneration, name='useropenAiContentGeneration'),
]
