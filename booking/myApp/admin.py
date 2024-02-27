from django.contrib import admin
from .models import Hotel, Room, Booking, Review, Transaction, Customer, Convenience
admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(Customer)
admin.site.register(Convenience)
admin.site.register(Booking)
admin.site.register(Review)
admin.site.register(Transaction)
