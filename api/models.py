# api/models.py
from django.db import models
from django.contrib.auth.models import User

class UploadHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    upload_time = models.DateTimeField(auto_now_add=True)
    total_count = models.IntegerField()
    avg_flowrate = models.FloatField()
    avg_pressure = models.FloatField()
    avg_temperature = models.FloatField()
    type_distribution = models.JSONField()
    raw_data = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ['-upload_time']

    def __str__(self):
        if self.user:
            return f"Upload at {self.upload_time.strftime('%Y-%m-%d %H:%M')} by {self.user.username}"
        return f"Upload at {self.upload_time.strftime('%Y-%m-%d %H:%M')}"