from django.urls import path
from .views import CustomTokenObtainPairView, UserRegistrationView, get_staff_users
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegistrationView.as_view(), name='user_register'),
    path('staff-list/', get_staff_users, name='staff_list'),  # New endpoint
]
