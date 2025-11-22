import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import UploadHistory

# Create 10 dummy entries
for i in range(10):
    UploadHistory.objects.create(
        total_count=random.randint(10, 100),
        avg_flowrate=random.uniform(1.0, 10.0),
        avg_pressure=random.uniform(10.0, 100.0),
        avg_temperature=random.uniform(20.0, 80.0),
        type_distribution={'Pump': 5, 'Valve': 5},
        raw_data=[]
    )

print(f"Total history items: {UploadHistory.objects.count()}")
