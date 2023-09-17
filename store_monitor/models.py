from django.db import models

# Create your models here.

class Store(models.Model):
    store_id = models.PositiveIntegerField(unique=True)
    timezone_str = models.CharField(max_length=50, default='America/Chicago')

class BusinessHours(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    day_of_week = models.PositiveIntegerField(choices=[(i, i) for i in range(7)])
    start_time_local = models.TimeField()
    end_time_local = models.TimeField()

class StoreStatus(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    timestamp_utc = models.DateTimeField()
    status = models.CharField(max_length=10, choices=[('active', 'active'), ('inactive', 'inactive')])
