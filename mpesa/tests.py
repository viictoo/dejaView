from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Transaction
from rest_framework.test import APIClient
from rest_framework import status


class TransactionModelTest(TestCase):
    """Tests For the Transaction Model"""
    def setUp(self):
        """Create a test user and test transaction"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.transaction = Transaction.objects.create(
            phone_number='+1234567890',
            checkout_request_id='test_checkout_request_id',
            reference='test_reference',
            description='Test transaction description',
            amount='10.00',
            status=1,
            receipt_no='test_receipt_no',
            ip='127.0.0.1',
        )

    def tearDown(self):
        """Clean up created objects after each test"""
        User.objects.all().delete()
        Transaction.objects.all().delete()

    def test_transaction_model_str(self):
        """Test the string representation of the Transaction model."""
        self.assertEqual(
            str(self.transaction), str(self.transaction.transaction_no))

    def test_transaction_model_fields(self):
        """Test the fields and values of the Transaction model."""
        self.assertEqual(self.transaction.phone_number, '+1234567890')
        self.assertEqual(
            self.transaction.checkout_request_id, 'test_checkout_request_id')
        self.assertEqual(self.transaction.reference, 'test_reference')
        self.assertEqual(
            self.transaction.description, 'Test transaction description')
        self.assertEqual(self.transaction.amount, '10.00')
        self.assertEqual(self.transaction.status, 1)
        self.assertEqual(self.transaction.receipt_no, 'test_receipt_no')
        self.assertEqual(self.transaction.ip, '127.0.0.1')


class MpesaCheckoutViewTest(TestCase):
    """Test Mpesa Checkout Endpoint
    """
    def setUp(self):
        self.client = APIClient()

    def test_mpesa_checkout_view(self):
        # Create a test user
        user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )


        # Create a test transaction data
        transaction_data = {
            "phone_number": "+1234567890",
            "checkout_request_id": "test_checkout_request_id",
            "reference": "test_reference",
            "description": "Test transaction description",
            "amount": "10.00",
            "status": 1,
            "receipt_no": "test_receipt_no",
            "ip": "127.0.0.1",
        }

        response = self.client.post(
            '/checkout/', data=transaction_data, format='json')

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST)

class MpesaCallBackViewTest(TestCase):
    """Test Mpesa Callback Endpoint"""
    def setUp(self):
        self.client = APIClient()

    def test_mpesa_callback_view_get(self):
        response = self.client.get('/callback/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"status": "OK"})

    def test_mpesa_callback_view_post(self):
        # Add your test data and assertions for the POST request handling
        pass

class CheckTransactionStatusViewTest(TestCase):
    """Test Transaction Status Endpoint"""
    def setUp(self):
        self.client = APIClient()

    def test_check_transaction_status_view(self):
        # Create a test transaction
        transaction = Transaction.objects.create(
            phone_number='+1234567890',
            checkout_request_id='test_checkout_request_id',
            reference='test_reference',
            description='Test transaction description',
            amount='10.00',
            status=1,
            receipt_no='test_receipt_no',
            ip='127.0.0.1',
        )

        response = self.client.get(
            f'/check_transaction_status/?checkout_request_id={transaction.checkout_request_id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"transaction_status": 1})
