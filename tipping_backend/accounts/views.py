from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from .models import CustomUser
from .serializers import CustomTokenObtainPairSerializer, CustomUserRegistrationSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserRegistrationSerializer


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import CustomUser
from .serializers import CustomUserSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def get_staff_users(request):
    """
    Retrieve all users with the 'staff' role.
    """
    staff_users = CustomUser.objects.filter(role='staff')
    serializer = CustomUserSerializer(staff_users, many=True)
    return Response(serializer.data)
