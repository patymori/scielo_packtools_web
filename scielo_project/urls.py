from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('stylechecker.urls', namespace='stylechecker')),
    path('admin/', admin.site.urls),
]
