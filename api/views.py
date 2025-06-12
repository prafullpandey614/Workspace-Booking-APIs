from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.contrib.auth.models import User
from django.utils.timezone import make_aware
from datetime import datetime, time
from django.shortcuts import get_object_or_404
from .models import Room, Booking, UserProfile, Team, TeamMember
from .serializers import BookingSerializer, BookingCreateSerializer, RoomAvailabilitySerializer, UserSerializer, TeamMemberSerializer, TeamSerializer, RoomSerializer, AvailableSlotsSerializer
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination

class UserRegistration(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            profile = UserProfile.objects.create(user=user, name=user.username, age=request.data.get('age',18), gender=request.data.get('gender','Male'))

            return Response({
                "message": "User registered successfully.",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "name": profile.name,
                    "age": profile.age,
                    "gender": profile.gender
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateTeamAPIView(ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class TeamMembershipAPIView(ListCreateAPIView):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer


class CreateRoomAPIView(ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class BookingView(APIView):
    """
    POST: Book a room.
    GET: View all bookings.
    """

    def get(self, request):
        bookings = Booking.objects.select_related('room', 'user', 'team').all()
        serializer = BookingSerializer(bookings, many=True)
        paginator = PageNumberPagination()
        paginated_rooms = paginator.paginate_queryset(bookings, request)

        serialized_rooms = BookingSerializer(paginated_rooms, many=True)
        return paginator.get_paginated_response(serialized_rooms.data)


    @transaction.atomic
    def post(self, request):
        serializer = BookingCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data

        checkin = validated['checkin_time']
        checkout = validated['checkout_time']
        room_type = request.data.get('room_type', 'PRIVATE')
        user = validated.get('user')
        team = validated.get('team')

        if not (time(9, 0) <= checkin.time() <= time(17, 0)) or not (time(9, 0) <= checkout.time() <= time(18, 0)):
            return Response({"detail": "Bookings must be between 9 AM and 6 PM."}, status=status.HTTP_400_BAD_REQUEST)

        if checkin >= checkout:
            return Response({"detail": "Checkout time must be after check-in time."}, status=status.HTTP_400_BAD_REQUEST)

        overlap_filter = Q(checkin_time__lt=checkout, checkout_time__gt=checkin)

        if user:
            if Booking.objects.filter(user=user).filter(overlap_filter).exists():
                return Response({"detail": "User already has a booking in this time range."}, status=status.HTTP_400_BAD_REQUEST)

            if room_type == 'PRIVATE':
                room = Room.objects.filter(room_type='PRIVATE').exclude(
                    booking__in=Booking.objects.filter(overlap_filter)
                ).first()
                if room:
                    booking = Booking.objects.create(room=room, user=user, checkin_time=checkin, checkout_time=checkout)
                    return Response({"booking_id": booking.id}, status=status.HTTP_201_CREATED)

            elif room_type == 'SHARED_DESK':
                rooms = Room.objects.filter(room_type='SHARED_DESK')
                for room in rooms:
                    count = Booking.objects.filter(room=room).filter(overlap_filter).count()
                    if count < room.capacity:
                        booking = Booking.objects.create(room=room, user=user, checkin_time=checkin, checkout_time=checkout)
                        return Response({"booking_id": booking.id}, status=status.HTTP_201_CREATED)

        elif team:
            if Booking.objects.filter(team=team).filter(overlap_filter).exists():
                return Response({"detail": "Team already has a booking in this time range."}, status=status.HTTP_400_BAD_REQUEST)

            members = TeamMember.objects.filter(team=team).select_related('user')
            headcount = sum(1 for m in members if m.user.age >= 10)

            if room_type == 'CONFERENCE' and len(members) >= 3:
                room = Room.objects.filter(
                    room_type='CONFERENCE',
                    capacity__gte=headcount
                ).exclude(
                    booking__in=Booking.objects.filter(overlap_filter)
                ).first()
                if room:
                    booking = Booking.objects.create(room=room, team=team, checkin_time=checkin, checkout_time=checkout)
                    return Response({"booking_id": booking.id}, status=status.HTTP_201_CREATED)

        return Response({"detail": "No available room for the selected time and type."}, status=status.HTTP_400_BAD_REQUEST)

class CancelBooking(APIView):
    """
    POST: Cancel a booking by ID.
    """

    def post(self, request, booking_id):
        try:
            booking = Booking.objects.get(id=booking_id)
            booking.delete()
            return Response({"detail": "Booking cancelled."})
        except Booking.DoesNotExist:
            return Response({"detail": "Booking not found."}, status=status.HTTP_404_NOT_FOUND)


class AvailableRoomsView(APIView):
    """
    GET: View available rooms for a specific slot (check-in and check-out) and room type.
    """

    def get(self, request):
        
        serializer = RoomAvailabilitySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        checkin = serializer.validated_data['checkin_time']
        checkout = serializer.validated_data['checkout_time']
        room_type = serializer.validated_data['room_type']
        available_rooms = []

        if room_type in ['PRIVATE', 'CONFERENCE']:
            rooms = Room.objects.filter(room_type=room_type)
            for room in rooms:
                # Check if room is free in given time range
                overlapping_bookings = Booking.objects.filter(
                    room=room,
                    checkin_time__lt=checkout,
                    checkout_time__gt=checkin
                )
                if not overlapping_bookings.exists():
                    available_rooms.append({
                        "room_id": room.id,
                        "available_desks": room.capacity - overlapping_count
                    })

        elif room_type == 'SHARED_DESK':
            rooms = Room.objects.filter(room_type='SHARED_DESK')
            for room in rooms:
                overlapping_count = Booking.objects.filter(
                    room=room,
                    checkin_time__lt=checkout,
                    checkout_time__gt=checkin
                ).count()
                if overlapping_count < room.capacity:
                    available_rooms.append({
                        "room_id": room.id,
                        "available_desks": room.capacity - overlapping_count
                    })
        paginator = PageNumberPagination()
        paginated_rooms = paginator.paginate_queryset(available_rooms, request)

        serialized_rooms = AvailableSlotsSerializer(paginated_rooms, many=True)
        return paginator.get_paginated_response(serialized_rooms.data)
