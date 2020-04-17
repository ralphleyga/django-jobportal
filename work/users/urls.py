from django.urls import path

from .views import ProfileUpdateView

app_name = 'users'

urlpatterns = [
    path('update/<int:pk>/', ProfileUpdateView.as_view(), name='update'),
]