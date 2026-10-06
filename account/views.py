from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import (
    UserRegistrationForm,
    UserEditForm,
    ProfileEditForm
)
from .models import Profile

from django.contrib import messages

class CustomLoginView(auth_views.LoginView):
    def form_valid(self, form):

        messages.success(
            self.request,
            f'hello, { form.get_user().username }.'
            )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "invalid username or password"
            )
        return super().form_invalid(form)

class CustomPasswordResetView(auth_views.PasswordResetView):
    def form_valid(self, form):

        messages.success(
            self.request,
            'email was successfully sent'
            )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "there was error while sending link"
            )
        return super().form_invalid(form)

class CustomPasswordChangeView(auth_views.PasswordChangeView):
    def form_valid(self, form):
        messages.success(
            self.request,
            'password was changed successfully'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            'there was error while changing password'
        )

        return super().form_invalid(form)

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)

            new_user.set_password(
                user_form.cleaned_data.get('password')
            )

            new_user.save()

            Profile.objects.create(user = new_user)

            messages.success(
                request,
                'register successful'
            )

            return render(
                request,
                'account/register_done.html',
                {
                    'new_user' : new_user
                }
            )
        else:
            error_msg = '; '.join([f"{error}" for errors in user_form.errors.values() for error in errors]).lower()
            messages.error(
                request,
                f'error: { error_msg }'
            )
    else:
        user_form = UserRegistrationForm()
    return render(
        request,
        'account/register.html',
        {
            'user_form' : user_form
        }
    )
@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(
            instance=request.user,
            data = request.POST
        )
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data = request.POST,
            files = request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(
                request,
                'profile was successfully updated'
            )
            return redirect('account:edit')
        else:
            messages.error(
                request,
                'error updating your profile'
            )
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(
        request,
        'account/edit.html',
        {
            'user_form' : user_form,
            'profile_form' : profile_form
        }
    )