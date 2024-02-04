from django.contrib import admin
from .models import Hotel, Room, User, Booking, Review, Transaction, Facility

admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(User)
admin.site.register(Booking)
admin.site.register(Review)
admin.site.register(Transaction)
admin.site.register(Facility)
