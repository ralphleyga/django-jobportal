from django.urls import path

from .views import ProfileUpdateView

app_name = 'users'

urlpatterns = [
    path('update/<int:id>/', ProfileUpdateView.as_view(), name='update'),
]