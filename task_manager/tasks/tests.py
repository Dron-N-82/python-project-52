import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Task
from ..statuses.models import Status

User = get_user_model()

@pytest.fixture
def login(client):
    user1 = User.objects.create_user(
        username='auth', password='ComplexPass123!'
        )
    user2 = User.objects.create_user(
        username='exec', password='ComplexPass123!'
        )
    client.login(username='auth', password='ComplexPass123!')
    status = Status.objects.create(name='Новая задача')
    return client, user1, user2, status

@pytest.mark.django_db
class Test_Tasks:
    def test_view_tasks(self, login):
        self.client, self.user1, self.user2, self.status = login
        response = self.client.get(reverse('tasks'))
        assert response.status_code == 200
        assert Task.objects.count() == 0

    def test_create_task(self, login):
        self.client, self.user1, self.user2, self.status = login
        # status = Status.objects.create(name='Новая задача')
        assert Task.objects.count() == 0
        response = self.client.post(
            reverse('task_create'),
            {'name': 'Задача',
            'author': self.user1.id,
            'status': self.status.id})
        assert response.status_code == 302
        # assert Status.objects.filter(name='Новая задача').exists()
        assert Task.objects.count() == 1

    def test_update_task(self, login):
        self.client, self.user1, self.user2, self.status = login
        # status = Status.objects.create(name='Новая задача')
        task = Task.objects.create(
            name='Задача',
            author=self.user1,
            status=self.status,
            executor=self.user2
            )
        update_url = reverse("task_update", kwargs={"id": task.pk})
        # update_url = reverse("task_update", args=[task.pk])
        response = self.client.post(
            update_url, {
                'name': 'UPD задача',

                'status': self.status.id
                }
            )
        assert response.status_code == 302
        task.refresh_from_db()
        assert task.name == "UPD задача"

    def test_delete_task_by_author(self, login):
        self.client, self.user1, self.user2, self.status = login
        task = Task.objects.create(
            name='Задача',
            author=self.user1,
            status=self.status,
            executor=self.user2
            )
        delete_url = reverse("task_delete", kwargs={"id": task.pk})
        response = self.client.post(delete_url)
        
        assert not Task.objects.filter(id=task.pk).exists()
        assert response.status_code == 302

    def test_delete_task_by_non_author(self, login):
        self.client, self.user1, self.user2, self.status = login
        task = Task.objects.create(
            name='Задача',
            author=self.user2,
            status=self.status,
            executor=self.user1
            )
        delete_url = reverse("task_delete", kwargs={"id": task.pk})
        response = self.client.post(delete_url)
        assert Task.objects.count() == 1
        assert Task.objects.filter(id=task.pk).exists()
                

    '''
    assert Task.objects.count() == 0
            status = Status.objects.create(name='Новая задача')
            task = Task.objects.create(
                name='Задача',
                author=self.user,
                status=status
                )
    '''