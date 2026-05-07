from django.db import models
from django.contrib.auth.models import User

class Meeting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    date_time = models.DateTimeField()
    emails = models.TextField(help_text="Separate emails with commas")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
