from django.urls import reverse  
from rest_framework import status  
from rest_framework.test import APITestCase, APIClient  # Import APIClient  
from rest_framework_simplejwt.tokens import RefreshToken  
from django.contrib.auth.models import User  
from .models import DaySchedule, TimeSlot  


class ScheduleAPITestCase(APITestCase):  
    @classmethod  
    def setUpTestData(cls):  
        # Create test user once for all tests  
        cls.user = User.objects.create_user(username='testuser', password='testpass')  
        
    def setUp(self):  
        # Initialize APIClient and set auth header  
        self.client = APIClient()  
        refresh = RefreshToken.for_user(self.user)  
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')  

        # Create initial DaySchedule instance  
        slot = TimeSlot.objects.create(start="00:00", stop="01:00", ids=[1, 2])  
        self.day_schedule = DaySchedule.objects.create(day="monday")  
        self.day_schedule.time_slots.add(slot)  

    def test_create_schedule(self):  
        # Test creating a new schedule object  
        url = reverse('schedule-list')  
        data = {  
            "day": "tuesday",  
            "time_slots": [  
                {"start": "01:00", "stop": "02:00", "ids": [3, 4]}  
            ]  
        }  
        response = self.client.post(url, data, format='json')  
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  
        self.assertEqual(DaySchedule.objects.count(), 2)  
        self.assertEqual(DaySchedule.objects.get(day="tuesday").time_slots.count(), 1)  

    def test_retrieve_schedule(self):  
        # Test retrieving a schedule object  
        url = reverse('schedule-detail', args=[self.day_schedule.id])  
        response = self.client.get(url, format='json')  
        self.assertEqual(response.status_code, status.HTTP_200_OK)  
        self.assertEqual(response.data['day'], 'monday')  

    def test_list_schedules(self):  
        # Test listing schedule objects  
        url = reverse('schedule-list')  
        response = self.client.get(url, format='json')  
        self.assertEqual(response.status_code, status.HTTP_200_OK)  
        self.assertEqual(len(response.data), 1)  # Initially one schedule in the setup  

    def test_update_schedule(self):  
        # Test updating a schedule object  
        url = reverse('schedule-detail', args=[self.day_schedule.id])  
        data = {  
            "day": "wednesday",  
            "time_slots": [  
                {"start": "02:00", "stop": "03:00", "ids": [5, 6]},  
                {"start": "03:00", "stop": "04:00", "ids": [7]}  
            ]  
        }  
        response = self.client.put(url, data, format='json')  
        self.assertEqual(response.status_code, status.HTTP_200_OK)  
        self.assertEqual(DaySchedule.objects.get(id=self.day_schedule.id).day, 'wednesday')  
        self.assertEqual(DaySchedule.objects.get(day="wednesday").time_slots.count(), 2)  

    def test_delete_schedule(self):  
        # Test deleting a schedule object  
        url = reverse('schedule-detail', args=[self.day_schedule.id])  
        response = self.client.delete(url, format='json')  
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)  
        self.assertEqual(DaySchedule.objects.count(), 0)  # No schedules should remain  
