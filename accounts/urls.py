from django.urls import path, include
from . import views
app_name = 'accounts'

urlpatterns = [
    path('<str:username>-<int:user_id>/profile', views.UserProfileView.as_view(), name='user_profile'),
]
