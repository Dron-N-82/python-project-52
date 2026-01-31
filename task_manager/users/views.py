# from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.urls import reverse
from django.contrib import messages, auth
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth import authenticate #, login
from task_manager.users.models import User
from .forms import CreateUserForm, LoginUserForm
from django.utils.translation import gettext as _



# Create your views here.
# class IndexView(TemplateView):
#     template_name = 'users/index.html'


class IndexView(View):
    def get(self, request, *args, **kwargs):
        # users = User.objects.all()
        users = User.objects.filter(is_superuser=0)
        context = {"users": users}
        return render(request, "users/index.html", context)
    

class CreateUserView(View):
    # если метод POST, то мы обрабатываем данные
    def post(self, request, *args, **kwargs):
        form = CreateUserForm(request.POST)  # Получаем данные формы из запроса
        if form.is_valid():  # Проверяем данные формы на корректность
            form.save()
            messages.success(request, _('The user is registered'))
            return redirect(reverse('login'))
        return render(request, "users/create.html", {"form": form})
        

    # если метод GET, то создаем пустую форму
    def get(self, request, *args, **kwargs):
        form = CreateUserForm()  # Создаем экземпляр нашей формы
        return render(
            request, "users/create.html", {"form": form}
        )  # Передаем нашу форму в контексте


class LoginUserView(View):
    def get(self, request, *args, **kwargs):
        form = LoginUserForm()
        return render(
            request,
            "users/login.html",
            {'form': form}
            )
    
    def post(self, request, *args, **kwargs):
        form = LoginUserForm(request.POST)  # Получаем данные формы из запроса
        if form.is_valid():  # Проверяем данные формы на корректность
            username = form.cleaned_data['username']
            # password = form.cleaned_data['password']
            password = form.cleaned_data['password1']
            user = auth.authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                messages.success(request, _('You have logged in successfully'))
                return redirect('index')
            else:
                messages.error(request, _('Incorrect username or password'))
                # form.add_error(None, 'Неверное имя пользователя или пароль')
                                
        else:
            form = LoginUserForm()

        return render(request, "users/login.html", {"form": form})
    

class LogoutUserView(View):
    def post(self, request):
        auth.logout(request)
        messages.info(request, _("You're out"))
        return redirect('index')
    

class AuthRequiredMessageMixin:
    login_url = 'login'  
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _('You are not logged in! Please log in.'))
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)


class UpdateUserView(AuthRequiredMessageMixin, LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        # user = User.objects.get(id=user_id)
        user = get_object_or_404(User, id=user_id)
        form = CreateUserForm(instance=user)
        if request.user.pk != user.pk:
            messages.error(request, _("You can only change your user's details!"))
            return redirect('users')
        return render(
            request,
            "users/update.html",
            {"form": form, 'user_id': user_id}
        )
    
    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        # user = User.objects.get(id=user_id)
        user = get_object_or_404(User, id=user_id)
        form = CreateUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, _('User data has been updated'))
            return redirect('users')
        return render(
            request,
            "users/update.html",
            {"form": form, 'user_id': user_id}
        )
    

class DeleteUserView(AuthRequiredMessageMixin, LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        # user = User.objects.get(id=user_id)
        user = get_object_or_404(User, id=user_id)
        if request.user.pk != user.pk:
            messages.error(request, _('You can only delete your own user!'))
            return redirect('users')
        return render(
            request,
            "users/delete.html",
            {'user': user}
            )

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get("id")
        # user = User.objects.get(id=user_id)
        user = get_object_or_404(User, id=user_id)
        if user:
            user.delete()
            messages.info(request, _('The user has been deleted'))
        return redirect('index')