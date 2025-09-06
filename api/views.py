# api/views.py
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.utils import timezone
from rest_framework import viewsets, status, mixins, serializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

from .models import Patient, Doctor, PatientDoctorMap
from .serializers import RegisterSerializer, PatientSerializer, DoctorSerializer, MappingSerializer
from .permissions import IsOwnerOrReadOnly

User = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]
    
    def post(self, request):
        # Rate limiting for registration
        ip_address = request.META.get('REMOTE_ADDR')
        cache_key = f"register_attempts_{ip_address}"
        attempts = cache.get(cache_key, 0)
        
        if attempts >= 5:  # Max 5 registration attempts per hour
            return Response(
                {"error": "Too many registration attempts. Please try again later."}, 
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            
            # Increment attempts counter
            cache.set(cache_key, attempts + 1, 3600)  # 1 hour
            
            return Response({
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'name': user.first_name
                },
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(TokenObtainPairView):
    throttle_classes = [AnonRateThrottle]
    
    def post(self, request, *args, **kwargs):
        # Rate limiting for login attempts
        ip_address = request.META.get('REMOTE_ADDR')
        cache_key = f"login_attempts_{ip_address}"
        attempts = cache.get(cache_key, 0)
        
        if attempts >= 10:  # Max 10 login attempts per hour
            return Response(
                {"error": "Too many login attempts. Please try again later."}, 
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 401:
            # Increment failed attempts counter
            cache.set(cache_key, attempts + 1, 3600)  # 1 hour
        else:
            # Reset counter on successful login
            cache.delete(cache_key)
            
        return response

class RefreshTokenView(TokenRefreshView):
    throttle_classes = [UserRateThrottle]

class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]
    queryset = Patient.objects.all()  # Required for DRF
    throttle_classes = [UserRateThrottle]
    
    def get_queryset(self):
        return Patient.objects.filter(created_by=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def perform_update(self, serializer):
        # Ensure user can only update their own patients
        if serializer.instance.created_by != self.request.user:
            raise serializers.ValidationError("You can only update your own patients.")
        serializer.save()
    
    def perform_destroy(self, instance):
        # Ensure user can only delete their own patients
        if instance.created_by != self.request.user:
            raise serializers.ValidationError("You can only delete your own patients.")
        instance.delete()

class DoctorViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]
    queryset = Doctor.objects.all()
    throttle_classes = [UserRateThrottle]

class PatientDoctorMappingViewSet(viewsets.ModelViewSet):
    serializer_class = MappingSerializer
    permission_classes = [IsAuthenticated]
    queryset = PatientDoctorMap.objects.all()  # Required for DRF
    throttle_classes = [UserRateThrottle]
    
    def get_queryset(self):
        return PatientDoctorMap.objects.filter(patient__created_by=self.request.user)
    
    def perform_create(self, serializer):
        # Validate that the patient belongs to the requesting user
        patient = serializer.validated_data['patient']
        if patient.created_by != self.request.user:
            raise serializers.ValidationError("You can only map doctors to your own patients.")
        serializer.save()
    
    def perform_update(self, serializer):
        # Ensure user can only update their own mappings
        if serializer.instance.patient.created_by != self.request.user:
            raise serializers.ValidationError("You can only update your own patient-doctor mappings.")
        serializer.save()
    
    def perform_destroy(self, instance):
        # Ensure user can only delete their own mappings
        if instance.patient.created_by != self.request.user:
            raise serializers.ValidationError("You can only delete your own patient-doctor mappings.")
        instance.delete()
