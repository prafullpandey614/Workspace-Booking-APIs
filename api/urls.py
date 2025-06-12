from django.contrib import admin
from django.urls import path,include
from .views import BookingView, CancelBooking, AvailableRoomsView, UserRegistration, CreateRoomAPIView,CreateTeamAPIView

urlpatterns = [
    path('api/v1/register/', UserRegistration.as_view()),  
    path('api/v1/bookings/', BookingView.as_view()),        
    path('api/v1/create-room/', CreateRoomAPIView.as_view()),        
    path('api/v1/create-team/', CreateTeamAPIView.as_view()),        
    path('api/v1/cancel/<int:booking_id>/', CancelBooking.as_view()),  
    path('api/v1/rooms/available/', AvailableRoomsView.as_view()),     
]
