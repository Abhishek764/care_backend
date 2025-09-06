from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.html import strip_tags
from rest_framework import serializers
from .models import Patient, Doctor, PatientDoctorMap

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    name = serializers.CharField(max_length=150, source='first_name')

    class Meta:
        model = User
        fields = ("id", "username", "email", "name", "password", "password_confirm")

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match.")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        return User.objects.create_user(**validated_data)

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ("id", "first_name", "last_name", "email", "date_of_birth", "phone", "created_at", "updated_at")
        read_only_fields = ("created_at", "updated_at")

    def validate_email(self, value):
        # Check for email uniqueness
        if Patient.objects.filter(email=value).exists():
            raise serializers.ValidationError("A patient with this email already exists.")
        return value

    def validate_phone(self, value):
        # Basic phone validation
        if value and len(value) < 10:
            raise serializers.ValidationError("Phone number must be at least 10 digits.")
        return value

    def validate_first_name(self, value):
        # XSS protection - strip HTML tags
        return strip_tags(value).strip()

    def validate_last_name(self, value):
        # XSS protection - strip HTML tags
        return strip_tags(value).strip()

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ("id", "first_name", "last_name", "email", "specialization", "created_at", "updated_at")
        read_only_fields = ("created_at", "updated_at")

    def validate_email(self, value):
        # Check for email uniqueness
        if Doctor.objects.filter(email=value).exists():
            raise serializers.ValidationError("A doctor with this email already exists.")
        return value

    def validate_specialization(self, value):
        # Basic specialization validation
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Specialization must be at least 3 characters.")
        return value.strip()

    def validate_first_name(self, value):
        # XSS protection - strip HTML tags
        return strip_tags(value).strip()

    def validate_last_name(self, value):
        # XSS protection - strip HTML tags
        return strip_tags(value).strip()

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