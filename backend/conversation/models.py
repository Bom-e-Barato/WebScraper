from django.db import models

from account.models import Account

# Create your models here.
class Conversation(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="sender_conversations")
    receiver = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="receiver_conversations")
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField()