import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from ..tasks.models import Task
from .models import Status

User = get_user_model()

# Create your tests here.


@pytest.fixture
def login(client):
    user = User.objects.create_user(
        username='test', password='ComplexPass123!'
        )
    client.login(username='test', password='ComplexPass123!')
    return client, user


@pytest.mark.django_db
class Test_Status:
    def test_read_statuses(self, login):
        self.client, self.user = login
        response = self.client.get(reverse('statuses'))
        assert response.status_code == 200

    def test_create_status(self, login):
        self.client, self.user = login
        assert Status.objects.count() == 0
        response = self.client.post(
            reverse('status_create'),
            {'name': 'Новая задача'})
        assert response.status_code == 302
        assert Status.objects.filter(name='Новая задача').exists()
        assert Status.objects.count() == 1
        
    def test_update_status(self, login):
        self.client, self.user = login
        status = Status.objects.create(name='Новая задача')
        # update_url = reverse("status_update", kwargs={"id": status.pk})
        update_url = reverse("status_update", args=[status.pk])
        response = self.client.post(
            update_url,
            {'name': 'Новая задача1'}
            )
        assert response.status_code == 302
        status.refresh_from_db()
        assert status.name == "Новая задача1"

    def test_delete_status_without_task(self, login):
        self.client, self.user = login
        status = Status.objects.create(name='Новая задача')
        # delete_url = reverse("status_delete", kwargs={"id": status.pk})
        delete_url = reverse("status_delete", args=[status.pk])
        response = self.client.post(delete_url)
        assert not Status.objects.filter(id=status.pk).exists()
        assert response.status_code == 302
        
    def test_delete_status_with_task(self, login):
        self.client, self.user = login
        status = Status.objects.create(name='Новая задача')
        Task.objects.create(
            name='Задача',
            author=self.user,
            status=status
            )
        delete_url = reverse("status_delete", args=[status.pk])
        response = self.client.post(delete_url)
        assert Status.objects.filter(id=status.pk).exists()
        assert response.status_code == 302