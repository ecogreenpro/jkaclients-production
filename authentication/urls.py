from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import path

from authentication import views

app_name = 'authentication'
urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('sign-up/', views.sign_up, name='sign_up'),
    path('verify-otp/', views.otp_verify, name='otp_verify'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('forgot-password/identity/', views.recover_password_otp_verify, name='recover_password_otp_verify'),
    path('forgot-password/resend-otp/', views.recover_password_resend_otp, name='recover_password_resend_otp'),
    path('forgot-password/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='authentication/reset-password.html',
                                          success_url='/'), name='recover-password-done'),
    path('my-team/', views.my_team, name='my_team'),
    path('account/update/', views.account_update, name='account_update'),
    path('change_password/', views.account_change_password, name='account_change_password'),
    path('account-setting/', views.account_settings, name='account_settings')
]
