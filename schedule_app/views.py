from rest_framework import viewsets  
from rest_framework_simplejwt.authentication import JWTAuthentication  
from rest_framework.permissions import IsAuthenticated  
from .models import DaySchedule  
from .serializers import DayScheduleSerializer  

class DayScheduleViewSet(viewsets.ModelViewSet):  
    queryset = DaySchedule.objects.all()  
    serializer_class = DayScheduleSerializer  
    permission_classes = [IsAuthenticated]  # JWT required  
    authentication_classes = [JWTAuthentication]  
