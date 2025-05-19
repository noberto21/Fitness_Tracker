from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'fitness'

urlpatterns = [
    # Main app views
    path('', views.dashboard, name='dashboard'),
    path('workout/create/', views.create_workout, name='create_workout'),
    path('workout/<int:workout_id>/add-exercise/', views.add_exercise, name='add_exercise'),
    path('workout/<int:workout_id>/', views.view_workout, name='view_workout'),
    path('profile/', views.profile, name='profile'),
    path('progress/', views.view_progress, name='view_progress'),

    # Authentication views
    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/signup/', views.signup, name='signup'),
    
    # Password reset views
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt'
    ), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
]