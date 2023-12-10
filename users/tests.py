# Create your tests here.
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.urls import reverse


class ProfileModelTest(TestCase):
    """unittests for the Profile Model"""
    def setUp(self):
        """Create a test user"""
        self.test_user = User.objects.create(
            username='django', password='Brunhilda')
        """Fetch a test profile created by signals"""
        self.test_profile = Profile.objects.get(user=self.test_user)

    def tearDown(self):
        """Clean up by deleting the test user"""
        self.test_user.delete()

    def test_profile_creation(self):
        """Test that a Profile instance is created when a User is created"""
        self.assertIsInstance(self.test_profile, Profile)
        self.assertEqual(
            str(self.test_profile), f'{self.test_user.username} Profile')

    def test_profile_fields(self):
        """Test individual fields of the Profile model"""
        self.assertEqual(self.test_profile.user, self.test_user)
        self.assertEqual(self.test_profile.phone_number, None)
        self.test_profile.phone_number = "12312123123"
        self.assertEqual(self.test_profile.phone_number, "12312123123")
        self.test_profile.phone_number = "12312123"
        self.assertEqual(self.test_profile.phone_number, "12312123")
        self.assertEqual(self.test_profile.image.name, 'default.jpg')

    def test_profile_str_method(self):
        """Test the __str__ method of the Profile model"""
        expected_str = f'{self.test_user.username} Profile'
        self.assertEqual(str(self.test_profile), expected_str)


class UserRegisterFormTest(TestCase):
    """FORMS: unittests for the user registration form"""
    def test_user_register_form_valid(self):
        """register user with valid data"""
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'phone_number': '+12345678903',
        }
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_register_form_invalid(self):
        """register user with invalid email"""
        form_data = {
            'username': 'testuser',
            'email': 'invalidemail',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'phone_number': '+1234567890',
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())


class UserUpdateFormTest(TestCase):
    """FORMS: unittests for the user update form"""
    def test_user_update_form_valid(self):
        """Test With Valid Form Data"""
        user = User.objects.create_user(
            username='testuser', password='testpassword')
        form_data = {
            'username': 'updateduser',
            'email': 'updateduser@example.com',
            'image': 'default.jpg',
            'phone_number': '+254712123123',
        }
        form = UserUpdateForm(instance=user, data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_update_form_invalid(self):
        """Test Empty username"""
        user = User.objects.create_user(
            username='testuser', password='testpassword')
        form_data = {
            'username': '',
            'email': 'updateduser@example.com',
            'image': 'default.jpg',
            'phone_number': '+254712123123',
        }
        form = UserUpdateForm(instance=user, data=form_data)
        self.assertFalse(form.is_valid())


class ProfileUpdateFormTest(TestCase):
    """"FORMS: test update phone number"""
    def test_profile_update_form_valid(self):
        """TEST profile update with valid data"""
        user = User.objects.create_user(
            username='testuser', password='testpassword')
        profile = user.profile
        form_data = {
            'username': 'testuser',
            'email': 'updateduser@example.com',
            'image': 'default.jpg',
            'phone_number': '+254712123123',
        }
        form = ProfileUpdateForm(instance=profile, data=form_data)
        self.assertTrue(form.is_valid())

    def test_profile_update_form_invalid(self):
        """TEST, profile update with invalid phone number"""
        user = User.objects.create_user(
            username='testuser', password='testpassword')
        profile = user.profile
        form_data = {
            'username': 'testuser',
            'email': 'updateduser@example.com',
            'image': 'default.jpg',
            'phone_number': 'invalidphonenumber',
        }
        form = ProfileUpdateForm(instance=profile, data=form_data)
        self.assertFalse(form.is_valid())


class RegisterViewTest(TestCase):
    """VIEWS: Tests for New User Registration View using Django client"""

    def test_register_view_get(self):
        """TEST:200 get the user registration view"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertIsInstance(response.context['form'], UserRegisterForm)

    def test_register_view_post_valid(self):
        """TEST: 302 Redirect on success"""
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'phone_number': '+254712123456',
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Profile.objects.count(), 1)

    def test_register_view_post_invalid(self):
        """Test: No Redirect Invalid email: 200 CODE: Form validation failed"""
        data = {
            'username': 'testuser',
            'email': 'invalidemail',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertIsInstance(response.context['form'], UserRegisterForm)


class ProfileViewTest(TestCase):
    """VIEWS: Tests for Profile View using Django client"""
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def tearDown(self):
        self.client.logout()

    def test_profile_view_get(self):
        """Tests GET view"""
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertIsInstance(response.context['u_form'], UserUpdateForm)
        self.assertIsInstance(response.context['p_form'], ProfileUpdateForm)

    def test_profile_view_post_valid(self):
        """Test 302 Redirect on success"""
        data = {
            'username': 'updateduser',
            'email': 'updateduser@example.com',
        }
        response = self.client.post(reverse('profile'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profile'))
        self.assertEqual(
            User.objects.get(username='updateduser').username, 'updateduser')

    def test_profile_view_post_invalid(self):
        """Empty username 200 # Form validation failed"""
        data = {
            'username': '',
            'email': 'updateduser@example.com',
        }
        response = self.client.post(reverse('profile'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertIsInstance(response.context['u_form'], UserUpdateForm)
        self.assertIsInstance(response.context['p_form'], ProfileUpdateForm)
