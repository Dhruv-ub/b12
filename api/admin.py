from django.contrib import admin
from .models import UploadHistory

# This tells the Admin panel: "Please show the UploadHistory table!"
@admin.register(UploadHistory)
class UploadHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'upload_time', 'total_count', 'avg_pressure') # Columns to show in the list
    list_filter = ('upload_time',) # Add a filter sidebar
    ordering = ('-upload_time',) # Newest first
