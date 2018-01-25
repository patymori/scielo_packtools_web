from django.urls import path

from .views import XMLValidateView


app_name = 'stylechecker'
urlpatterns = [
    path('', XMLValidateView.as_view(), name='xml-validator')
]
