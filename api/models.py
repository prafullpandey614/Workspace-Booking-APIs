from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    GENDER_TYPES = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10,choices=GENDER_TYPES)

class Room(models.Model):
    ROOM_TYPES = [
        ('PRIVATE', 'Private'),
        ('CONFERENCE', 'Conference'),
        ('SHARED_DESK', 'Shared Desk'),
    ]
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    capacity = models.IntegerField()

    def __str__(self):
        return f"{self.room_type} {self.id} - Capacity: {self.capacity} "

class Team(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"

class TeamMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.team.name}"


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    checkin_time = models.DateTimeField(null=True, blank=True)
    checkout_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking: {self.room} by {self.user or self.team} from {self.checkin_time} to {self.checkout_time}"


