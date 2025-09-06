from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

from .models import Patient, Doctor, PatientDoctorMap

User = get_user_model()

class HealthcareAPITests(APITestCase):

    def setUp(self):
        # Create users
        self.user = User.objects.create_user(username="testuser", password="pass123")
        self.other_user = User.objects.create_user(username="otheruser", password="pass123")

        # Authenticate testuser
        self.client.login(username="testuser", password="pass123")

        # Create doctors
        self.doctor1 = Doctor.objects.create(first_name="John", last_name="Smith", email="doc1@example.com", specialization="Cardiology")
        self.doctor2 = Doctor.objects.create(first_name="Alice", last_name="Brown", email="doc2@example.com", specialization="Dermatology")

        # Create patients
        self.patient1 = Patient.objects.create(first_name="Bob", last_name="Lee", email="bob@example.com", created_by=self.user)
        self.patient2 = Patient.objects.create(first_name="Tom", last_name="Cruise", email="tom@example.com", created_by=self.other_user)

    def test_register_user(self):
        url = reverse("register")
        data = {"username": "newuser", "password": "pass123"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_user(self):
        url = reverse("login")
        data = {"username": "testuser", "password": "pass123"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_create_patient(self):
        url = reverse("patient-list")
        data = {"first_name": "New", "last_name": "Patient", "email": "newpatient@example.com"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_map_patient_to_doctor(self):
        url = reverse("mappings-list")  # ✅ Correct name from router
        data = {"patient": self.patient1.id, "doctor": self.doctor1.id}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_prevent_duplicate_patient_doctor_mapping(self):
        url = reverse("mappings-list")  # ✅ Correct name
        data = {"patient": self.patient1.id, "doctor": self.doctor1.id}
        self.client.post(url, data, format="json")  # first mapping
        response = self.client.post(url, data, format="json")  # duplicate
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "This patient is already mapped to this doctor.")
