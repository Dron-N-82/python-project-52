from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.urls import reverse
from django.contrib import messages, auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from django.db.models import ProtectedError

from task_manager.statuses.models import Status
from .forms import CreateStatusForm

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
        template_name = 'statuses/index.html'
        statuses = Status.objects.all()
        context = {"statuses": statuses}
        return render(request, template_name, context)
    

class CreateStatusView(AuthRequiredMessageMixin, LoginRequiredMixin, View):
    # если метод POST, то мы обрабатываем данные
    def post(self, request, *args, **kwargs):
        form = CreateStatusForm(request.POST)  # Получаем данные формы из запроса
        if form.is_valid():  # Проверяем данные формы на корректность
            form.save()
            messages.success(request, _('Status successfully created'))
            return redirect(reverse('statuses'))
        return render(request, "statuses/create.html", {"form": form})
        

    # если метод GET, то создаем пустую форму
    def get(self, request, *args, **kwargs):
        form = CreateStatusForm()  # Создаем экземпляр нашей формы
        return render(
            request, "statuses/create.html", {"form": form}
        )  # Передаем нашу форму в контексте


class UpdateStatusView(AuthRequiredMessageMixin, LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        status_id = kwargs.get('id')
        status = get_object_or_404(Status, id=status_id)
        form = CreateStatusForm(instance=status)
        # if request.user.pk != user.pk:
        #     messages.error(request, _("You can only change your statuses details!"))
        #     return redirect('statuses')
        return render(
            request,
            "statuses/update.html",
            {"form": form, 'status_id': status_id}
        )
    
    def post(self, request, *args, **kwargs):
        status_id = kwargs.get('id')
        status = get_object_or_404(Status, id=status_id)
        form = CreateStatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            messages.success(request, _('Status data has been updated'))
            return redirect('statuses')
        return render(
            request,
            "statuses/update.html",
            {"form": form, 'status_id': status_id}
        )
    

class DeleteStatusView(AuthRequiredMessageMixin, LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        status_id = kwargs.get('id')
        status = get_object_or_404(Status, id=status_id)
        return render(
            request,
            "statuses/delete.html",
            {'status': status}
            )

    def post(self, request, *args, **kwargs):
        status_id = kwargs.get("id")
        status = get_object_or_404(Status, id=status_id)
        if status:
            try:
                # Попытка удалить статус
                status.delete()
            except ProtectedError:
                # Если возникла ошибка ProtectedError, покажите сообщение и перенаправьте
                messages.error(request, _('The status cannot be deleted because it is used in tasks'))
                # Невозможно удалить статус, потому что он используется в задачах."
                return redirect('statuses')
            # status.delete()
        messages.info(request, _('The status has been deleted'))
        return redirect('statuses')