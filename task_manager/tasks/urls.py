from django.urls import path

from task_manager.tasks import views

urlpatterns = [
    path("", views.IndexView.as_view(), name='tasks'),
    path('create/', views.CreateTaskView.as_view(), name='task_create'),
    path('<int:id>/update/', views.UpdateTaskView.as_view(), name='task_update'),
    path('<int:id>/delete/', views.DeleteTaskView.as_view(), name='task_delete'),
    path('<int:id>/', views.ViewTaskView.as_view(), name='task_view'),
]