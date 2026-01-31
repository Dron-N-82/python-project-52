from django.urls import path

from task_manager.labels import views

urlpatterns = [
    path("", views.IndexView.as_view(), name='labels'),
    path('create/', views.CreateLabelView.as_view(), name='label_create'),
    path('<int:id>/update/', views.UpdateLabelView.as_view(), name='label_update'),
    path('<int:id>/delete/', views.DeleteLabelView.as_view(), name='label_delete'),
]