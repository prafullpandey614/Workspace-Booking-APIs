from django.contrib import admin
from .models import UserProfile, Room, Team, TeamMember, Booking

admin.site.register(UserProfile)
admin.site.register(Room)
admin.site.register(Team)
admin.site.register(Booking)

