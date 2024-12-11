from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('ci.urls')),  
    path('auth/', include('auth_service.urls')),  
]
