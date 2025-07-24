from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Patient, Hospital, TypeCheckPoint
from .views import CheckPointViewSet
from users.models import CardioUser
from datetime import date
import pytest


class PatientModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Patient.objects.create(code="PT234", gender="Мужской")

    def test_code_label(self):
        patient = Patient.objects.get(id=1)
        field_label = patient._meta.get_field("code").verbose_name
        self.assertEquals(field_label, "Идентификатор пациента")

    # Сравним  макисмальную длину кода пациента
    def test_code_max_length(self):
        patient = Patient.objects.get(id=1)
        max_length = patient._meta.get_field("code").max_length
        self.assertEquals(max_length, 128)

    # Проверим, действительно ли мы ожидаем строкове представление класса в виде кода
    def test_object_name_is_code(self):
        patient = Patient.objects.get(id=1)
        expected_object_name = patient.code
        self.assertEquals(expected_object_name, str(patient))


class PatientViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.patient1 = Patient.objects.create(
            code="P001", gender="Женский", birth=date(1990, 5, 15)
        )
        self.patient2 = Patient.objects.create(
            code="P002", gender="Мужской", birth=date(1985, 10, 20)
        )
        self.patient3 = Patient.objects.create(
            code="P003", gender="Женский", birth=date(1995, 3, 10)
        )
        self.list_url = reverse("patient-list")
        self.export_url = reverse("patient-export-csv")

    def test_get_all_patients(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_filter_by_code(self):
        response = self.client.get(f"{self.list_url}?code=P001")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["code"], "P001")

    def test_filter_by_gender_icontains(self):
        # Проверяем частичное совпадение
        response = self.client.get(f"{self.list_url}?gender=жен")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertTrue(all(p["gender"] == "Женский" for p in response.data))

    def test_filter_by_birth(self):
        test_date = "1990-05-15"
        response = self.client.get(f"{self.list_url}?birth={test_date}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["code"], "P001")

    def test_multiple_filters(self):
        url = f"{self.list_url}?gender=Женский&birth__gte=1990-01-01"  # gte - больше или равно
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertTrue(all(p["gender"] == "Женский" for p in response.data))

    def test_unauthenticated_access(self):
        self.client.credentials()  # Удаляем аутентификацию
        response = self.client.get(self.list_url)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )  # IsAuthenticatedOrReadOnly разрешает GET


@pytest.mark.django_db
def test_checkpoint_list():
    client = APIClient()
    response = client.get("/renal_denervation/check-points/")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_CRUD():
    user = CardioUser.objects.create_user(username="test user")
    client = APIClient()
    client.force_authenticate(user=user)

    patient = Patient.objects.create(code="test patient", gender="Мужской")
    hospital = Hospital.objects.create(fullname="test hospital")
    type_point = TypeCheckPoint.objects.create(name="test check_point")

    data = {
        "patient": patient.id,
        "hospital_id": hospital.id,
        "type_point": type_point.id,
        "date_of_receipt": "2018-04-01",
        "date_of_discharge": "2018-04-01",
    }

    create_resp = client.post("/renal_denervation/check-points/", data, format="json")
    assert create_resp.status_code == 201
    created_id = create_resp.data["id"]

    # Тест чтения
    get_resp = client.get(f"/renal_denervation/check-points/{created_id}/")
    assert get_resp.status_code == 200
    assert get_resp.data["patient"] == patient.id

    # Тест обновления
    update_data = {"date_of_receipt": "2017-04-01"}
    update_resp = client.patch(
        f"/renal_denervation/check-points/{created_id}/", update_data, format="json"
    )
    assert update_resp.status_code == 200
    assert update_resp.data["date_of_receipt"] == "2017-04-01"

    # Тест удаления
    del_resp = client.delete(f"/renal_denervation/check-points/{created_id}/")
    assert del_resp.status_code == 204

    # Проверка, что запись удалена
    verify_resp = client.get(f"/renal_denervation/check-points/{created_id}/")
    assert verify_resp.status_code == 404
