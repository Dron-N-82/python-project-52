from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.urls import reverse
from django.contrib import messages, auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _

from task_manager.tasks.models import Task
from .forms import CreateTaskForm, ViewTaskForm

# Create your views here.
class AuthRequiredMessageMixin:
    login_url = 'login'  
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _('You are not logged in! Please log in.'))
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)


class IndexView(AuthRequiredMessageMixin, LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        template_name = 'tasks/index.html'
        tasks = Task.objects.all()
        # print(tasks)
        context = {"tasks": tasks}
        return render(request, template_name, context)
    

class CreateTaskView(AuthRequiredMessageMixin, LoginRequiredMixin, View):
    # если метод POST, то мы обрабатываем данные
    def post(self, request, *args, **kwargs):
        form = CreateTaskForm(request.POST)  # Получаем данные формы из запроса
        if form.is_valid():  # Проверяем данные формы на корректность
            task = form.save(commit=False) # создаем объект без сохранения
            task.author = request.user     # добавляем автора
            form.save()
            messages.success(request, _('Task successfully created'))
            return redirect(reverse('tasks'))
        return render(request, "tasks/create.html", {"form": form})
        

    # если метод GET, то создаем пустую форму
    def get(self, request, *args, **kwargs):
        form = CreateTaskForm()  # Создаем экземпляр нашей формы
        return render(
            request, "tasks/create.html", {"form": form}
        )
    

class UpdateTaskView(AuthRequiredMessageMixin, LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('id')
        task = get_object_or_404(Task, id=task_id)
        form = CreateTaskForm(instance=task)
        # if request.user.pk != user.pk:
        #     messages.error(request, _("You can only change your statuses details!"))
        #     return redirect('statuses')
        return render(
            request,
            "tasks/update.html",
            {"form": form, 'task_id': task_id}
        )
    
    def post(self, request, *args, **kwargs):
        task_id = kwargs.get('id')
        task = get_object_or_404(Task, id=task_id)
        form = CreateTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, _('Task data has been updated'))
            return redirect('tasks')
        return render(
            request,
            "tasks/update.html",
            {"form": form, 'task_id': task_id}
        )
    

class DeleteTaskView(AuthRequiredMessageMixin, LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('id')
        task = get_object_or_404(Task, id=task_id)
        if request.user.pk != task.author.pk:
            messages.error(request, _('A task can only be deleted by its author'))
            return redirect('tasks')
        return render(
            request,
            "tasks/delete.html",
            {'task': task}
                )
        

    def post(self, request, *args, **kwargs):
        task_id = kwargs.get("id")
        task = get_object_or_404(Task, id=task_id)
        print(request.user.pk)
        print(task.author.pk)
        if task:
            task.delete()
            messages.info(request, _('The task has been deleted'))
        return redirect('tasks')
    

class ViewTaskView(AuthRequiredMessageMixin, LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('id')
        task = get_object_or_404(Task, id=task_id)
        print(task)
        # form = ViewTaskForm(instance=task)
        return render(
            request,
            "tasks/task.html",
            {'task': task}
        )