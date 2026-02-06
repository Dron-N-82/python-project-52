from django.urls import path

from task_manager.statuses import views

urlpatterns = [
    path("",
         views.IndexView.as_view(),
         name='statuses'),
    path('create/',
         views.CreateStatusView.as_view(),
         name='status_create'),
    path('<int:id>/update/',
         views.UpdateStatusView.as_view(),
         name='status_update'),
    path('<int:id>/delete/',
         views.DeleteStatusView.as_view(),
         name='status_delete'),
]