

# Create your tests here.
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, Products, Bid

class UserSignupTest(APITestCase):
    def test_renter_signup(self):
        url = reverse('user-signup')
        data = {
            "type": "renter",
            "email": "renter@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "password": "password123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], "User created successfully")

    def test_lender_signup(self):
        url = reverse('user-signup')
        data = {
            "type": "lender",
            "email": "lender@example.com",
            "first_name": "Jane",
            "last_name": "Smith",
            "password": "password123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], "User created successfully")

class ProductsListingTest(APITestCase):
    def setUp(self):
        # Create a lender user
        self.lender = User.objects.create_user(
            email="lender@example.com",
            password="password123",
            first_name="Lender",
            last_name="One",
            user_type="lender"
        )
        self.client.force_authenticate(user=self.lender)

    def test_Products_listing(self):
        url = reverse('Products-list')
        data = {
            "item_name": "Laptop",
            "item_description": "A high-end gaming laptop",
            "quote_price_per_month": 150.0,
            "item_category": "Electronic Appliances"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], "Products listed successfully")

class BidTest(APITestCase):
    def setUp(self):
        # Create a lender and renter user
        self.lender = User.objects.create_user(
            email="lender@example.com",
            password="password123",
            first_name="Lender",
            last_name="One",
            user_type="lender"
        )
        self.renter = User.objects.create_user(
            email="renter@example.com",
            password="password123",
            first_name="Renter",
            last_name="Two",
            user_type="renter"
        )
        # Create a Products
        self.Products = Products.objects.create(
            item_name="Laptop",
            item_description="A high-end gaming laptop",
            quote_price_per_month=150.0,
            item_category="Electronic Appliances",
            lender=self.lender
        )
        self.client.force_authenticate(user=self.renter)

    def test_place_bid(self):
        url = reverse('place-bid', kwargs={'Products_id': self.Products.id})
        data = {
            "bid_price_per_month": 160.0,
            "bid_duration": 3  # Months
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], "Bid placed successfully")
