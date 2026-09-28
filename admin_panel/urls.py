from django.urls import path
from .views import dashboard_super_admin

urlpatterns = [
    path('', dashboard_super_admin, name='dashboard_admin'),
]