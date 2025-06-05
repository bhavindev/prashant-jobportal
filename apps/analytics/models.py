from django.db import models

class Visitor(models.Model):
    count = models.IntegerField(default=0)
    os = models.CharField(max_length=50, blank=True, null=True)
    browser = models.CharField(max_length=50, blank=True, null=True)
    device = models.CharField(max_length=50, blank=True, null=True)
    visited_at = models.DateTimeField(blank=True, null=True, auto_now=True)
    
    def __str__(self):
        return f'Visitor {self.pk}' 
