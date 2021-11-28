from django.urls import path
from django.conf import settings
from facial_app.api import views
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('feedback/', views.FeedbackAPIView.as_view(), name='feedback'),
    path('create_attendance/', views.CreateAttendanceAPIView.as_view(), name='create_attendance'),
    path('list_attendance/', views.ListAttendanceAPIView.as_view(), name='list_attendance'),
    path('delete_attendance/<int:pk>/', views.DeleteAttendanceAPIView.as_view(), name='delete_attendance'),
    path('take_attendance/', views.TakeAttendanceAPIView.as_view(), name='take_attendance'),
]

router = DefaultRouter()
router.register("attendance_list", views.SearchAttendanceViewSet, basename="attendance_list")
urlpatterns += router.urls
