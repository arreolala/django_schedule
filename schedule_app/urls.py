from rest_framework.routers import DefaultRouter  
from .views import DayScheduleViewSet  

router = DefaultRouter()  
router.register(r'schedules', DayScheduleViewSet, basename='schedule')  

urlpatterns = router.urls  
