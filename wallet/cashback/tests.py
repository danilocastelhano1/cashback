import base64

from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.test import APITestCase


class RentalTests(APITestCase):
    def setUp(self) -> None:
        self.data = {
            "sold_at": "2021-01-02 00:00:00",
            "customer": {"document": "88462165040", "name": "Test Case"},
            "total": "115.99",
            "products": [
                {"type": "A", "value": "10.00", "qty": 1},
                {"type": "C", "value": "10.00", "qty": 9},
                {"type": "B", "value": "15.99", "qty": 1},
            ],
        }
        self.user = User.objects.create_user(
            username=settings.USERNAME, password=settings.PASSWORD
        )
        self.credentials = base64.b64encode(
            f"{settings.USERNAME}:{settings.PASSWORD}".encode("utf-8")
        )

    def test_without_authorization(self):
        resp = self.client.get("/api/cashback/")
        self.assertEqual(resp.status_code, 401)

    def test_should_error_when_passing_invalid_data(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Basic {}".format(self.credentials.decode("utf-8"))
        )

        self.data["sold_at"] = "202-01-02 00:00:00"
        resp = self.client.post("/api/cashback/", data=self.data, format="json")
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(
            resp.json()["sold_at"][0],
            "Datetime has wrong format. Use one of these formats instead: "
            "YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].",
        )

    def test_should_error_when_passing_invalid_cpf(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Basic {}".format(self.credentials.decode("utf-8"))
        )

        self.data["sold_at"] = "2022-01-02 00:00:00"
        self.data["customer"]["document"] = "12345678901"

        resp = self.client.post("/api/cashback/", data=self.data, format="json")
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()["customer"]["document"][0], "Invalid CPF")

    def test_should_error_when_passing_invalid_total(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Basic {}".format(self.credentials.decode("utf-8"))
        )

        self.data["total"] = "10.99"

        resp = self.client.post("/api/cashback/", data=self.data, format="json")
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(
            resp.json()["products"][0], "Total does not match with the sum of products"
        )

    def test_should_error_when_passing_invalid_type(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Basic {}".format(self.credentials.decode("utf-8"))
        )

        self.data["products"][0]["type"] = "E"

        resp = self.client.post("/api/cashback/", data=self.data, format="json")
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(
            resp.json()["products"][0]["type"][0], '"E" is not a valid choice.'
        )

    def test_should_create_a_cashback(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Basic {}".format(self.credentials.decode("utf-8"))
        )
        resp = self.client.post("/api/cashback/", data=self.data, format="json")
        self.assertEqual(resp.status_code, 201)
