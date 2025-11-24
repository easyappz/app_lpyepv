from django.urls import path
from api.views import (
    RegisterView,
    LoginView,
    ProfileView,
    MessageListView,
    MessageCreateView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('messages/', MessageListView.as_view(), name='messages-list'),
    path('messages/create/', MessageCreateView.as_view(), name='messages-create'),
]
