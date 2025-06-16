from django.test import TestCase
from .models import Status
from .forms import StatusForm
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm

User = get_user_model()

class UserViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
            email='test@example.com'
        )

    def test_user_list_view(self):
        response = self.client.get(reverse('users_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')

    def test_user_create_view(self):
        response = self.client.post(reverse('user_create'), {
            'username': 'newuser',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
            'email': 'new@example.com'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_update_view(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(reverse('user_update', args=[self.user.pk]), {
            'username': 'updateduser',
            'first_name': 'Updated',
            'last_name': 'User',
            'email': 'updated@example.com'
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')

    def test_user_delete_view(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(reverse('user_delete', args=[self.user.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())

    def test_login_view(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertFalse('_auth_user_id' in self.client.session)

class StatusViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.status = Status.objects.create(name='Test Status')
    
    def test_status_list_requires_login(self):
        response = self.client.get(reverse('statuses_list'))
        self.assertRedirects(response, '/login/?next=/statuses/')
    
    def test_status_create(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('status_create'), {'name': 'New Status'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name='New Status').exists())

    def test_status_update(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(
            reverse('status_update', args=[self.status.pk]),
            {'name': 'Updated Status'}
        )
        self.assertEqual(response.status_code, 302)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Updated Status')

    def test_status_delete(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('status_delete', args=[self.status.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Status.objects.filter(pk=self.status.pk).exists())

    def test_status_delete_protected(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('status_delete', args=[self.status.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(pk=self.status.pk).exists())