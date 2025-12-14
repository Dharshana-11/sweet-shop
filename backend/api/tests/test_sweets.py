from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from sweets.models import Sweet

class SweetsAuthTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username = "sweetuser",
            password = "sweet@123"
        )

        self.url = reverse("sweets-list")
    
    def test_sweets_requires_authentication(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class CreateSweetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username = "sweetuser",
            password = "sweet@123"
        )

        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION = f"Bearer {str(refresh.access_token)}"
        )

        self.url = reverse("sweets-list")
    
    def test_create_sweet(self):
        data = {
            "name": "Milk Peda",
            "category": "Indian",
            "price": 10.0,
            "quantity": 100
        }

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class SearchSweetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username = "sweetuser",
            password = "sweet@123"
        )

        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION = f"Bearer {str(refresh.access_token)}"
        )

        Sweet.objects.create(
            name = "Rasagulla",
            category = "Indian",
            price = 40,
            quantity = 50,
        )

        Sweet.objects.create(
            name = "Cake",
            category = "Bakery",
            price = 30,
            quantity = 20,
        )
        
        self.url = reverse("sweets-search")
    
    def test_search_sweet_by_category(self):

        response = self.client.get(self.url + "?category=Indian")
        self.assertEqual(len(response.data), 1) #Test only 1 record is returned for category India
        self.assertEqual(response.data[0]["name"],"Rasagulla") #Test whether the returned sweet is Rasagulla
    
    def test_search_sweet_by_price_range(self):
        response = self.client.get(self.url + "?min_price=35")
        self.assertEqual(len(response.data), 1)


class UpdateSweetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="sweetuser",
            password="sweet@123"
        )

        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )

        self.sweet = Sweet.objects.create(
            name="Rasagulla",
            category="Indian",
            price=40,
            quantity=50
        )

        self.url = reverse("sweets-update", args=[self.sweet.id])

    def test_authenticated_user_can_update_sweet(self):
        payload = {
            "name": "Rasamalai",
            "category": "Indian",
            "price": 30,
            "quantity": 15
        }

        response = self.client.put(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.sweet.refresh_from_db()
        self.assertEqual(self.sweet.name, payload["name"])
        self.assertEqual(self.sweet.price, payload["price"])
        self.assertEqual(self.sweet.quantity, payload["quantity"])


class DeleteSweetTest(APITestCase):

    def setUp(self):
        # Normal user
        self.user = User.objects.create_user(
            username="user",
            password="user@123"
        )

        # Admin user
        self.admin = User.objects.create_user(
            username="admin",
            password="admin@123",
            is_staff=True
        )

        self.sweet = Sweet.objects.create(
            name="Jalebi",
            category="Indian",
            price=20,
            quantity=30
        )

        self.url = reverse("sweets-delete", args=[self.sweet.id])

    def test_non_admin_cannot_delete_sweet(self):
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )

        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_delete_sweet(self):
        refresh = RefreshToken.for_user(self.admin)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )

        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Deleted sweet ID must not exist in DB
        self.assertFalse(
            Sweet.objects.filter(id=self.sweet.id).exists()
        )


class PurchaseSweetTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="buyer",
            password="buy@123"
        )

        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )

        self.sweet = Sweet.objects.create(
            name="Barfi",
            category="Indian",
            price=25,
            quantity=2
        )

        self.url = reverse("sweets-purchase", args=[self.sweet.id])

    def test_purchase_decreases_quantity(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.sweet.refresh_from_db()
        self.assertEqual(self.sweet.quantity, 1)

    def test_purchase_fails_when_out_of_stock(self):
        self.sweet.quantity = 0
        self.sweet.save()

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
