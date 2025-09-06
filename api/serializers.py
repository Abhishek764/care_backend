from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import Patient, Doctor, PatientDoctorMap

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    name = serializers.CharField(max_length=150, source='first_name')

    class Meta:
        model = User
        fields = ("id", "username", "email", "name", "password")

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class PatientSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source="created_by.id")

    class Meta:
        model = Patient
        fields = ("id", "first_name", "last_name", "email", "date_of_birth", "phone", "created_by", "created_at", "updated_at")
        read_only_fields = ("created_by", "created_at", "updated_at")

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ("id", "first_name", "last_name", "email", "specialization", "created_at", "updated_at")
        read_only_fields = ("created_at", "updated_at")

class MappingSerializer(serializers.ModelSerializer):
    patient_detail = PatientSerializer(source="patient", read_only=True)
    doctor_detail = DoctorSerializer(source="doctor", read_only=True)

    class Meta:
        model = PatientDoctorMap
        fields = ("id", "patient", "doctor", "patient_detail", "doctor_detail", "created_at")
        read_only_fields = ("created_at",)

    def validate(self, attrs):
        # Ensure the patient belongs to the requesting user
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            patient = attrs.get("patient")
            if patient and patient.created_by_id != request.user.id:
                raise serializers.ValidationError("You can only map doctors to your own patients.")
        return attrs