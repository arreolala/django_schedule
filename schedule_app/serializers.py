from rest_framework import serializers  
from .models import DaySchedule, TimeSlot  


class TimeSlotSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = TimeSlot  
        fields = ['start', 'stop', 'ids', 'camera_ids']  


class DayScheduleSerializer(serializers.ModelSerializer):  
    time_slots = TimeSlotSerializer(many=True)  

    class Meta:  
        model = DaySchedule  
        fields = ['day', 'time_slots']  

    def create(self, validated_data):  
        time_slots_data = validated_data.pop('time_slots')  
        day_schedule = DaySchedule.objects.create(**validated_data)  
        for slot_data in time_slots_data:  
            time_slot = TimeSlot.objects.create(**slot_data)  
            day_schedule.time_slots.add(time_slot)  
        return day_schedule  

    def update(self, instance, validated_data):  
        # Update the day  
        instance.day = validated_data.get('day', instance.day)  
        instance.save()  

        # If updating fully, remove old related time slots.  
        instance.time_slots.clear()  

        # Add new slots from provided data  
        time_slots_data = validated_data.pop('time_slots')  
        for slot_data in time_slots_data:  
            time_slot = TimeSlot.objects.create(**slot_data)  
            instance.time_slots.add(time_slot)  
        
        return instance  
