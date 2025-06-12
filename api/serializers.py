from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Booking, Room, Team, TeamMember
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

class BookingSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"

class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"

class BookingCreateSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = ["user","team","checkin_time", "checkout_time"]

class RoomAvailabilitySerializer(serializers.Serializer):
    checkin_time = serializers.DateTimeField()
    checkout_time = serializers.DateTimeField()
    room_type = serializers.ChoiceField(choices=Room.ROOM_TYPES)

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise ValidationError("Username already exists.")
        return value

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email', '')
        )
        user.set_password(validated_data['password'])  # hash password
        user.save()
        return user
    
class TeamSerializer(ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name']

class TeamMemberSerializer(ModelSerializer):
    class Meta:
        model = TeamMember
        fields = ['id', 'user', 'team']

class AvailableSlotsSerializer(serializers.Serializer):
    room_id = serializers.IntegerField()
    available_desks = serializers.IntegerField()