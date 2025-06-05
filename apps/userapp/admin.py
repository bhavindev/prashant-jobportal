from django.contrib import admin
from apps.userapp.models import *

@admin.register(supportTicket)
class supportTicketAdmin(admin.ModelAdmin):
    list_display = ['title', 'client', 'status', 'priority', 'created_at']
    
admin.site.register(TicketReply)