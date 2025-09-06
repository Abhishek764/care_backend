from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import PatientDoctorMap
from .serializers import MappingSerializer

from .views import (
    RegisterView, LoginView, RefreshTokenView,
    PatientViewSet, DoctorViewSet,
    PatientDoctorMappingViewSet
)

# ✅ Explicitly set basenames to match tests
router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename="patients")
router.register(r'doctors', DoctorViewSet, basename="doctors")
router.register(r'mappings', PatientDoctorMappingViewSet, basename="mappings")

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_doctors_by_patient(request, patient_id):
    """Get all doctors assigned to a specific patient"""
    mappings = PatientDoctorMap.objects.filter(
        patient_id=patient_id,
        patient__created_by=request.user
    )
    serializer = MappingSerializer(mappings, many=True)
    return Response(serializer.data)

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),

    # Patient-Doctor mapping by patient ID
    path('mappings/<int:patient_id>/', get_doctors_by_patient, name='mappings-by-patient'),

    # Include router URLs
    path('', include(router.urls)),
]
