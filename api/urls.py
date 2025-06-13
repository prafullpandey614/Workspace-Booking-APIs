from django.contrib import admin
from django.urls import path,include
from .views import BookingView, CancelBooking, AvailableRoomsView, UserRegistration, CreateRoomAPIView,CreateTeamAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/register/', UserRegistration.as_view()),  
    path('api/v1/bookings/', BookingView.as_view()),        
    path('api/v1/create-room/', CreateRoomAPIView.as_view()),        
    path('api/v1/create-team/', CreateTeamAPIView.as_view()),        
    path('api/v1/cancel/<int:booking_id>/', CancelBooking.as_view()),  
    path('api/v1/rooms/available/', AvailableRoomsView.as_view()),     
]
