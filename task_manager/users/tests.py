# import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
# from django.contrib.auth.models import User

User = get_user_model()

# Create your tests here.
# @pytest.mark.django_db
class UsersTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="test",
            first_name= 'New',
            last_name= 'User'
            )
        self.user.set_password('ComplexPass123!') 
        self.user.save()

    def test_users_list(self):
        response = self.client.get(reverse("users"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("users", response.context)
        users = response.context["users"]
        self.assertTrue(len(users) > 0)

    def test_user_registration(self):
        users_before = User.objects.count()
        url = reverse('user_create')  
        data = {
            'username': 'newuser',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
            'first_name': 'New',
            'last_name': 'User'
            }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, 302)

        self.assertTrue(User.objects.count() != users_before)
        # self.assertEqual(User.objects.count(), users_before + 1)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_update(self):
        self.client.login(username='test', password='ComplexPass123!')
        update_url = reverse("user_update", kwargs={"id": self.user.pk})
        list_url = reverse("users")

        response = self.client.post(
            update_url, data={
                "username": "newuser1",
                'password1': 'ComplexPass123!',
                'password2': 'ComplexPass123!',
                'first_name': 'New1',
                'last_name': 'User'
                }
            )

        response = self.client.get(list_url)

        self.user.refresh_from_db()
        self.assertContains(response, "newuser1")
        self.assertNotContains(response, "test")

    def test_user_delete(self):
        self.client.login(username='test', password='ComplexPass123!')
        url_delete = reverse('user_delete', kwargs={"id": self.user.pk})  
        response = self.client.post(url_delete)
        self.assertRedirects(response, reverse('index'))
        
        self.assertFalse(User.objects.filter(username='test').exists())

