from django.contrib import messages  # , auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views import View

from .forms import CreateLabelForm
from .models import Label


class AuthRequiredMessageMixin:
    login_url = 'login'  
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _('You are not logged in! Please log in.'))
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)


class IndexView(AuthRequiredMessageMixin, LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        template_name = 'labels/index.html'
        labels = Label.objects.all()
        context = {"labels": labels}
        return render(request, template_name, context)
    

class CreateLabelView(AuthRequiredMessageMixin, LoginRequiredMixin, View):
    # если метод POST, то мы обрабатываем данные
    def post(self, request, *args, **kwargs):
        form = CreateLabelForm(request.POST)  # Получаем данные формы из запроса
        if form.is_valid():  # Проверяем данные формы на корректность
            form.save()
            messages.success(request, _('Label successfully created'))
            return redirect(reverse('labels'))
        return render(request, "labels/create.html", {"form": form})

    # если метод GET, то создаем пустую форму
    def get(self, request, *args, **kwargs):
        form = CreateLabelForm()  # Создаем экземпляр нашей формы
        return render(
            request, "labels/create.html", {"form": form}
        )  # Передаем нашу форму в контексте
    

class UpdateLabelView(AuthRequiredMessageMixin, LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        label_id = kwargs.get('id')
        label = get_object_or_404(Label, id=label_id)
        form = CreateLabelForm(instance=label)
        return render(
            request,
            "labels/update.html",
            {"form": form, 'label_id': label_id}
        )
    
    def post(self, request, *args, **kwargs):
        label_id = kwargs.get('id')
        label = get_object_or_404(Label, id=label_id)
        form = CreateLabelForm(request.POST, instance=label)
        if form.is_valid():
            form.save()
            messages.success(request, _('Label data has been updated'))
            return redirect('labels')
        return render(
            request,
            "labels/update.html",
            {"form": form, 'label_id': label_id}
        )
    

class DeleteLabelView(AuthRequiredMessageMixin, LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        label_id = kwargs.get('id')
        label = get_object_or_404(Label, id=label_id)
        print(label)
        return render(
            request,
            "labels/delete.html",
            {'label': label}
            )

    def post(self, request, *args, **kwargs):
        label_id = kwargs.get("id")
        label = get_object_or_404(Label, id=label_id)
        if label.tasks.exists():
            messages.error(request,
                           _('The label cannot be '
                             'deleted because it is used in tasks'))
            return redirect('labels')
        label.delete()
        messages.info(request, _('The label has been deleted'))
        return redirect('labels')