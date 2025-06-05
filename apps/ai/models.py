from django.db import models
from apps.authapp.models import User


class OpenAIChatRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100, blank=True, null=True)
    user_input = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'OpenAI Chat Record - {self.timestamp}'