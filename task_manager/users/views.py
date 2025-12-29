# from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from django.contrib import messages
from task_manager.users.models import User
from .forms import CreateUserForm, LoginUserForm


# Create your views here.
# class IndexView(TemplateView):
#     template_name = 'users/index.html'


class IndexView(View):
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        context = {"users": users}
        return render(request, "users/index.html", context)
    

class CreateUserView(View):
    # если метод POST, то мы обрабатываем данные
    def post(self, request, *args, **kwargs):
        form = CreateUserForm(request.POST)  # Получаем данные формы из запроса
        if form.is_valid():  # Проверяем данные формы на корректность
            form.save()
            return redirect(reverse('login'))
        return render(request, "users/create.html", {"form": form})
        

    # если метод GET, то создаем пустую форму
    def get(self, request, *args, **kwargs):
        form = CreateUserForm()  # Создаем экземпляр нашей формы
        return render(
            request, "users/create.html", {"form": form}
        )  # Передаем нашу форму в контексте
    

class UpdateUserView(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = User.objects.get(id=user_id)
        form = CreateUserForm(instance=user)
        return render(
            request,
            "users/update.html",
            {"form": form, 'user_id': user_id}
        )
    
    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = User.objects.get(id=user_id)
        form = CreateUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('index')
                
        return render(
            request,
            "users/update.html",
            {"form": form, 'user_id': user_id}
        )
    

class DeleteUserView(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = User.objects.get(id=user_id)
        return render(
            request,
            "users/delete.html",
            {'user': user}
            )

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get("id")
        user = User.objects.get(id=user_id)
        if user:
            user.delete()
        return redirect('index')


class LoginUserView(View):
    def get(self, request, *args, **kwargs):
        form = LoginUserForm()
        return render(
            request,
            "users/login.html",
            {'form': form}
            )
    
    # def post(self, request, *args, **kwargs):
    #     form = LoginUserForm(request.POST)  # Получаем данные формы из запроса
    #     if form.is_valid():  # Проверяем данные формы на корректность
            
    #         return redirect(reverse('index'))
    #     return render(request, "users/login.html", {"form": form})