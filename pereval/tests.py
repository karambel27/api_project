from django.test import TestCase
from rest_framework.test import APIClient

from .models import PerevalAdded


class PerevalAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.data = {
            "beauty_title": "пер.",
            "title": "Пхия",
            "other_titles": "Триев",
            "connect": "",
            "add_time": "2021-09-22T13:18:13Z",
            "user": {
                "email": "qwerty@mail.ru",
                "fam": "Пупкин",
                "name": "Василий",
                "otc": "Иванович",
                "phone": "+7 555 55 55"
            },
            "coords": {
                "latitude": "45.3842",
                "longitude": "7.1525",
                "height": 1200
            },
            "level": {
                "winter": "",
                "summer": "1А",
                "autumn": "1А",
                "spring": ""
            },
            "images": [
                {
                    "data": "test_image",
                    "title": "Седловина"
                }
            ]
        }

    def test_create_pereval(self):
        response = self.client.post(
            "/submitData/",
            self.data,
            format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], 200)
        self.assertIsNone(response.data["message"])
        self.assertIsNotNone(response.data["id"])
        self.assertEqual(PerevalAdded.objects.count(), 1)

        pereval = PerevalAdded.objects.first()
        self.assertEqual(pereval.status, "new")
        self.assertEqual(pereval.title, "Пхия")

    def test_get_pereval_by_id(self):
        create_response = self.client.post(
            "/submitData/",
            self.data,
            format="json"
        )

        pereval_id = create_response.data["id"]

        response = self.client.get(f"/submitData/{pereval_id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], pereval_id)
        self.assertEqual(response.data["title"], "Пхия")
        self.assertEqual(response.data["status"], "new")

    def test_get_perevals_by_user_email(self):
        self.client.post(
            "/submitData/",
            self.data,
            format="json"
        )

        response = self.client.get(
            "/submitData/?user__email=qwerty@mail.ru"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["user"]["email"], "qwerty@mail.ru")

    def test_patch_pereval_when_status_new(self):
        create_response = self.client.post(
            "/submitData/",
            self.data,
            format="json"
        )

        pereval_id = create_response.data["id"]

        patch_data = {
            "title": "Пхия обновлённый",
            "other_titles": "Новое название"
        }

        response = self.client.patch(
            f"/submitData/{pereval_id}/",
            patch_data,
            format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["state"], 1)
        self.assertIsNone(response.data["message"])

        pereval = PerevalAdded.objects.get(id=pereval_id)
        self.assertEqual(pereval.title, "Пхия обновлённый")

    def test_patch_pereval_when_status_not_new(self):
        create_response = self.client.post(
            "/submitData/",
            self.data,
            format="json"
        )

        pereval_id = create_response.data["id"]

        pereval = PerevalAdded.objects.get(id=pereval_id)
        pereval.status = "accepted"
        pereval.save()

        patch_data = {
            "title": "Не должно измениться"
        }

        response = self.client.patch(
            f"/submitData/{pereval_id}/",
            patch_data,
            format="json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["state"], 0)

        pereval.refresh_from_db()
        self.assertNotEqual(pereval.title, "Не должно измениться")

    def test_patch_does_not_change_user_data(self):
        create_response = self.client.post(
            "/submitData/",
            self.data,
            format="json"
        )

        pereval_id = create_response.data["id"]

        patch_data = {
            "title": "Название изменилось",
            "user": {
                "email": "new@mail.ru",
                "fam": "Иванов",
                "name": "Иван",
                "otc": "Иванович",
                "phone": "+7 999 999 99 99"
            }
        }

        response = self.client.patch(
            f"/submitData/{pereval_id}/",
            patch_data,
            format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["state"], 1)

        pereval = PerevalAdded.objects.get(id=pereval_id)
        self.assertEqual(pereval.user.email, "qwerty@mail.ru")
        self.assertEqual(pereval.user.fam, "Пупкин")