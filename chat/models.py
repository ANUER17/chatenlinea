from django.contrib.auth.models import User
from django.db import models

class Friendship(models.Model):
    sender = models.ForeignKey(User, related_name='friendship_requests_sent', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='friendship_requests_received', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=(('pending', 'Pending'), ('accepted', 'Accepted')))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Friendship between {self.sender} and {self.receiver} ({self.status})"

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # Campo para controlar si el mensaje ha sido leído

    def __str__(self):
        return f"Message from {self.sender} to {self.recipient} at {self.timestamp}"

