from django.db import models

class YourModelName(models.Model):
    field_name = models.CharField(max_length=100)


class Message(models.Model):
    phone = models.CharField(max_length=15)  # Phone number
    message = models.TextField()  # Message content
    send_time = models.DateTimeField()  # Scheduled time
    status = models.CharField(max_length=10, default='pending')  # pending, sent, failed

    def __str__(self):
        return f"Message to {self.phone} at {self.send_time}"
