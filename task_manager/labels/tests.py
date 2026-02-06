import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from ..statuses.models import Status
from ..tasks.models import Task
from .models import Label

User = get_user_model()


@pytest.fixture
def login(client):
    user = User.objects.create_user(
        username='test', password='ComplexPass123!'
        )
    client.login(username='test', password='ComplexPass123!')
    return client, user


@pytest.mark.django_db
class Test_Label:
    def test_read_labels(self, login):
        self.client, self.user = login
        response = self.client.get(reverse('labels'))
        assert response.status_code == 200

    def test_create_label(self, login):
        self.client, self.user = login
        assert Label.objects.count() == 0
        response = self.client.post(
            reverse('label_create'),
            {'name': 'Новая метка'})
        assert response.status_code == 302
        assert Label.objects.filter(name='Новая метка').exists()
        assert Label.objects.count() == 1
        
    def test_update_label(self, login):
        self.client, self.user = login
        label = Label.objects.create(name='Новая метка')
        # update_url = reverse("label_update", kwargs={"id": label.pk})
        update_url = reverse("label_update", args=[label.pk])
        response = self.client.post(
            update_url,
            {'name': 'Новая метка1'}
            )
        assert response.status_code == 302
        label.refresh_from_db()
        assert label.name == "Новая метка1"

    def test_delete_label_without_task(self, login):
        self.client, self.user = login
        label = Label.objects.create(name='Новая метка')
        # delete_url = reverse("label_delete", kwargs={"id": label.pk})
        delete_url = reverse("label_delete", args=[label.pk])
        response = self.client.post(delete_url)
        assert not Label.objects.filter(id=label.pk).exists()
        assert response.status_code == 302
        
    def test_delete_label_with_task(self, login):
        self.client, self.user = login
        status = Status.objects.create(name='Новая задача')
        label = Label.objects.create(name='Новая метка')
        task = Task.objects.create(
            name='Задача',
            author=self.user,
            status=status
            )
        task.label.add(label)   # Добавляем метку к задаче
        delete_url = reverse("label_delete", args=[label.pk])
        response = self.client.post(delete_url)
        assert Label.objects.filter(id=label.pk).exists()
        assert response.status_code == 302
