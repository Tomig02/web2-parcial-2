from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'administration'
urlpatterns = [
    path('', views.my_custom_admin_view, name='custom_admin_dashboard'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('register/', views.register_view, name='register'),
    path('recovery/', views.recovery_view, name='recovery'),
    path('<int:pk>/edit/', views.edit_message, name='edit_message'),
    path('<int:pk>/delete/', views.delete_message, name='delete_message'),
    path("logout/", auth_views.LogoutView.as_view(), name="logout")
]


