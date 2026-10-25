from django.shortcuts import render, redirect
from members.models import Profile
from .forms import ProfileEditForm
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from allauth.account.forms import ChangePasswordForm, SetPasswordForm, AddEmailForm

from allauth.account.internal import flows
from allauth.account.internal.flows.email_verification import (
    send_verification_email_to_address,
)
from allauth.account.models import EmailAddress

from allauth.socialaccount.models import SocialAccount

from allauth.socialaccount import providers as socialaccount_providers

@login_required
def personal_info_edit(request):
    if request.method == 'POST':
        profile_form = ProfileEditForm(
                instance=request.user.profile,
                data = request.POST,
                files = request.FILES
                )
        
        if profile_form.is_valid():
            profile_form.save()
            messages.success(
                request,
                'profile was successfully updated'
            )
            return redirect('account_personal_info_edit')
        else:
            messages.error(
                request,
                'error while editing profile'
            )
    else:
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(
        request,
        'account_management/personal_info_edit.html',
        {
            'profile_form' : profile_form,
        }
    )

@login_required
def security_info_edit(request):
    user = request.user

    if user.has_usable_password():
        password_form = ChangePasswordForm(user=user)
        password_set_form = None
    else:
        password_form = None
        password_set_form = SetPasswordForm(user=user)

    email_form = AddEmailForm(
        user=user,
    )

    current_emailaddress = EmailAddress.objects.filter(
        user=user,
        primary=True,
    ).first()

    pending_email = EmailAddress.objects.filter(
        user=user,
        verified=False,
    ).exclude(primary=True).first()
    
    social_accounts = SocialAccount.objects.filter(
        user_id=request.user.id
    )

    connected_provider_ids = set(
        social_accounts.values_list("provider", flat=True)
    )

    available_provider_ids = [
        provider.id
        for provider in socialaccount_providers.registry.get_class_list()
        if provider.id not in connected_provider_ids
    ]

    if request.method == "POST":

        if "action_password" in request.POST:
            if user.has_usable_password():
                password_form = ChangePasswordForm(user=user, data=request.POST)
                if password_form.is_valid():
                    password_form.save()
                    flows.password_change.finalize_password_change(
                        request,
                        password_form.user,
                    )
                    return redirect("account_security_info_edit")
            else:
                password_set_form = SetPasswordForm(user=user, data=request.POST)
                if password_set_form.is_valid():
                    password_set_form.save()
                    flows.password_change.finalize_password_set(
                        request,
                        password_set_form.user,
                    )
                    return redirect("account_security_info_edit")

        elif "action_add" in request.POST:
            email_form = AddEmailForm(
                user=user,
                data=request.POST,
            )
            if email_form.is_valid():
                flows.manage_email.add_email(request, email_form)
                return redirect("account_security_info_edit")

        elif "action_send" in request.POST:
            email_value = request.POST.get("email")
            if email_value:
                email_address = EmailAddress.objects.filter(
                    user=user,
                    email=email_value,
                ).first()
                if email_address:
                    send_verification_email_to_address(request, email_address)
                    return redirect("account_security_info_edit")
            messages.error(request, "Email not found")
            return redirect("account_security_info_edit")

        elif "action_remove" in request.POST:
            email_value = request.POST.get("email")
            if email_value:
                email_address = EmailAddress.objects.filter(
                    user=user,
                    email=email_value,
                ).first() 
                if email_address:
                    flows.manage_email.delete_email(request, email_address)
                    return redirect("account_security_info_edit")
            messages.error(request, "Email not found")
            return redirect("account_security_info_edit")

        else:
            messages.error(request, "Unknown action")

    return render(
        request,
        "account_management/security_info_edit.html",
        {
            "password_form": password_form,
            "password_set_form": password_set_form,
            "email_form": email_form,
            "current_emailaddress": current_emailaddress,
            "new_emailaddress": pending_email,
            'social_accounts' : social_accounts,
            'available_provider_ids' : available_provider_ids,
        },
    )