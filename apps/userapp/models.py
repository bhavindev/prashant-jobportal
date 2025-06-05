from django.db import models
from apps.crm.models import crmProjects
from django.contrib.auth import get_user_model

class supportTicket(models.Model):
    TICKET_STATUS_CHOICE = (
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    )
    
    TICKET_PRIORITY_CHOICE = (
        ('minor', 'Minor'),
        ('major', 'Major'),
    )

    client = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    project = models.ForeignKey(crmProjects, on_delete=models.CASCADE)
    title = models.CharField(max_length=255,blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=TICKET_STATUS_CHOICE, default='open', blank=True, null=True)
    priority = models.CharField(max_length=50, choices=TICKET_PRIORITY_CHOICE, default='minor', blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    
    def statusBadge(self):
        if self.status == 'open':
            return 'primary' 
        elif self.status == 'closed':
            return 'danger' 
        elif self.status == 'in_progress':
            return 'warning'
        elif self.status == 'resolved':
            return 'success'
        else:
            return 'secondary'
        
    def priorityBadge(self):
        return 'danger' if self.priority == 'major' else 'warning'

    def __str__(self):
        return self.title
    
class TicketReply(models.Model):
    ticket = models.ForeignKey(supportTicket, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    reply = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return 'Reply by {} on {}'.format(self.user.username, self.ticket.title)

