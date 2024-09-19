from django.contrib import admin
from .models import Products, Bid, RentalAgreement, User  # Import the models you want to register

# Register your models here
admin.site.register(User)
admin.site.register(Products)
admin.site.register(Bid)
admin.site.register(RentalAgreement)
