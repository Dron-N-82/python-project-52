from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

User = get_user_model()

# Create your tests here.
class UsersTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="user"
            # first_name= 'New',
            # last_name= 'User'
            )
        self.user.set_password('ComplexPass123!')  # устанавливаем пароль
        self.user.save()  # сохраняем изменения
    
    def test_registration(self):
        # URL регистрации
        url = reverse('user_create')  # Укажите ваше URL по имени
        data = {
            'username': 'newuser',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
            'first_name': 'New',
            'last_name': 'User'
            }
        response = self.client.post(url, data)
        
        self.assertRedirects(response, reverse('login'))  # Или ваш URL
        # self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_users_list(self):
        response = self.client.get(reverse("users"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("users", response.context)
        users = response.context["users"]
        # Проверяем не пустой ли список пользователей
        self.assertTrue(len(users) > 0)

    def test_user_update(self):
        update_url = reverse("user_update", kwargs={"id": self.user.pk})
        list_url = reverse("users")

        self.client.post(
            update_url, data={
                "username": "newuser1",
                'password1': 'ComplexPass123!',
                'password2': 'ComplexPass123!',
                'first_name': 'New',
                'last_name': 'User'
                }
            )

        response = self.client.get(list_url)

        self.assertContains(response, "newuser")
        self.assertNotContains(response, "newuser1")
# class UserTest(TestCase):
#     pass
    '''
    def setUp(self):
        # Создаем пользователя для тестов логина/редактирования
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_registration(self):
        # URL регистрации
        url = reverse('user_create')  # Укажите ваше URL по имени
        data = {
            'username': 'newuser',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
            }
        response = self.client.post(url, data)
        # Проверяем, что произошел редирект (на логин или другую страницу)
        self.assertRedirects(response, reverse('login'))  # Или ваш URL
        # Проверяем, что пользователь создан
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_logout(self):
        login_url = reverse('login')
        logout_url = reverse('logout')

        # Логин успешный
        response = self.client.post(login_url, {'username': 'testuser', 'password': 'testpass123'})
        self.assertRedirects(response, reverse('some_title_or_home'))

        # Проверка, что пользователь залогинен
        user = User.objects.get(username='testuser')
        self.assertTrue(user.is_authenticated)

        # Логаут
        response = self.client.get(logout_url)
        # Обычно редирект после logout
        self.assertRedirects(response, reverse('login'))

    def test_user_edit(self):
        # Авторизация
        self.client.login(username='testuser', password='testpass123')
        url = reverse('profile_edit')  # замените на ваш URL
        data = {
            'username': 'modifieduser',
            'email': 'modified@example.com',
            # дополнительные поля
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('profile'))
        # Проверяем изменения
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'modifieduser')
        self.assertEqual(self.user.email, 'modified@example.com')

    def test_user_delete(self):
        # Авторизация
        self.client.login(username='testuser', password='testpass123')
        url = reverse('profile_delete')  # ваш URL для удаления
        response = self.client.post(url)
        self.assertRedirects(response, reverse('some_redirect_after_delete'))
        # Пользователь удален
        self.assertFalse(User.objects.filter(username='testuser').exists())
    '''