# api/views.py
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, mixins, serializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Patient, Doctor, PatientDoctorMap
from .serializers import RegisterSerializer, PatientSerializer, DoctorSerializer, MappingSerializer
from .permissions import IsOwnerOrReadOnly

User = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': RegisterSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(TokenObtainPairView):
    pass

class RefreshTokenView(TokenRefreshView):
    pass

class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]
    queryset = Patient.objects.all()  # Required for DRF
    
    def get_queryset(self):
        return Patient.objects.filter(created_by=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class DoctorViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]
    queryset = Doctor.objects.all()

class PatientDoctorMappingViewSet(viewsets.ModelViewSet):
    serializer_class = MappingSerializer
    permission_classes = [IsAuthenticated]
    queryset = PatientDoctorMap.objects.all()  # Required for DRF
    
    def get_queryset(self):
        return PatientDoctorMap.objects.filter(patient__created_by=self.request.user)
    
    def perform_create(self, serializer):
        # Validate that the patient belongs to the requesting user
        patient = serializer.validated_data['patient']
        if patient.created_by != self.request.user:
            raise serializers.ValidationError("You can only map doctors to your own patients.")
        serializer.save()
