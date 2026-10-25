from django.urls import path, include, re_path
from . import views

from allauth.account import views as allauth_views

urlpatterns = [
    path('login/', allauth_views.LoginView.as_view(), name = 'account_login'),
    path('login/code', allauth_views.RequestLoginCodeView.as_view(), name = 'account_request_login_code'),
    path('login/code/confirm', allauth_views.ConfirmLoginCodeView.as_view(), name = "account_confirm_login_code"),
    path('logout/', allauth_views.LogoutView.as_view(), name = 'account_logout'),
    path('signup/', allauth_views.SignupView.as_view(), name = 'account_signup'),
    path('password/reset/', allauth_views.PasswordResetView.as_view(), name = 'account_reset_password'),
    re_path(r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$", allauth_views.PasswordResetFromKeyView.as_view(), name="account_reset_password_from_key"),
    path("password/reset/done/", allauth_views.PasswordResetDoneView.as_view(), name="account_reset_password_done"),
    path("confirm-email/", allauth_views.EmailVerificationSentView.as_view(), name="account_email_verification_sent"),
    re_path(
                r"^confirm-email/(?P<key>[-:\w]+)/$",
                allauth_views.ConfirmEmailView.as_view(),
                name="account_confirm_email",
            ),

    # settings 
    path('settings/personal-info', views.personal_info_edit, name = 'account_personal_info_edit'),

    path('settings/security-info', views.security_info_edit, name = 'account_security_info_edit'),

    # path('accounts_test/', include('allauth.urls')),


    # google oauth2 login
    path("", include("allauth.socialaccount.providers.google.urls")),
]

