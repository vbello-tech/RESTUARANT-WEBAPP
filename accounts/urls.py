from django.urls import path, reverse_lazy
from .views import signup_view, UserDetailView, change_password, user_edit, profile_edit
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetCompleteView,
)

app_name = "account"

urlpatterns = [
    path('login/', LoginView.as_view(template_name='registrations/login.html'), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', signup_view, name="sign_up"),
    path('change-password/', change_password, name="change_password"),
    path('user/<int:pk>/', UserDetailView.as_view(), name="user_detail"),
    path('reset-password/', PasswordResetView.as_view(
        template_name='registrations/password_reset.html',
        success_url=reverse_lazy('account:password_reset_done')
    ), name="password_reset"),
    path('password-reset-done/', PasswordResetDoneView.as_view(template_name='registrations/password_reset_done.html'), name="password_reset_done"),
    path('password-reset-confirm/(<uidb64>)-(<token>)/', PasswordResetConfirmView.as_view(
        template_name='registrations/password_reset_confirm.html',
        success_url=reverse_lazy('account:password_reset_complete')
    ), name="password_reset_confirm"),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(template_name='registrations/password_reset_complete.html'),  name="password_reset_complete"),
    path('user/<int:pk>/user_edit/', user_edit, name="user_edit"),
    path('user/<int:pk>/profile_edit/', profile_edit, name="profile_edit"),
]