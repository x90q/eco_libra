from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from . import views


app_name = 'account'

urlpatterns = [
    path(
        'login/',
        views.CustomLoginView.as_view(),
        name = 'login'
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name = 'logout'
    ),
    path(
        'password-change/',
        views.CustomPasswordChangeView.as_view(
            success_url=reverse_lazy('account:password_change_done')
        ),
        name = 'password_change'
        ),
    path(
        'password-change/done/',
        auth_views.PasswordChangeDoneView.as_view(),
        name = 'password_change_done'
    ),
    path(
        'password-reset/',
        views.CustomPasswordResetView.as_view(
            success_url=reverse_lazy('account:password_reset_done')
        ),
        name = 'password_reset'
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(),
        name = 'password_reset_done',
    ),
    path(
        'password-reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            success_url=reverse_lazy('account:password_reset_complete')
        ),
        name='password_reset_confirm',
    ),
    path(
        'password-reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(),
        name = 'password_reset_complete'
    ),
    path('register/', views.register, name = 'register'),
    path('edit/', views.edit, name = 'edit'),
]