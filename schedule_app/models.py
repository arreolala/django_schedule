from django.db import models


class TimeSlot(models.Model):  
    start = models.TimeField()  
    stop = models.TimeField()  
    # Use JSONField for flexibility; store lists of IDs  
    ids = models.JSONField(blank=True, null=True)  
    # Optional field for future expansion or other data types  
    camera_ids = models.JSONField(blank=True, null=True)  


class DaySchedule(models.Model):  
    day = models.CharField(max_length=9, unique=True)  # Days are unique  
    time_slots = models.ManyToManyField(TimeSlot, related_name='day_schedules')  
