from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin route
    path('api/', include('commodity.urls')),  # Include URLs from the 'Products' app
]
