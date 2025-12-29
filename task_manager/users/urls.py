from django.urls import path

from task_manager.users import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # path("", views.index),
    path('create/', views.CreateUserView.as_view(), name='user_create'),
    path('<int:id>/update/', views.UpdateUserView.as_view(), name='user_update'),
    path('<int:id>/delete/', views.DeleteUserView.as_view(), name='user_delete'),
    # path('login/', views.LoginUserView.as_view(), name='user_login'),
]