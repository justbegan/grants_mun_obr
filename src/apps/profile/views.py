from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import UserForm, ProfileForm


def index(request):
    # if request.method == 'POST':
    #     user_form = UserForm(request.POST, instance=request.user)
    #     profile_form = ProfileForm(request.POST, instance=request.user.profile)
    #     if user_form.is_valid() and profile_form.is_valid():
    #         user_form.save()
    #         profile_form.save()
    #         messages.success(request, 'Ваш профиль был успешно обновлен!')
    #         return redirect('profile-home')
    #     else:
    #         messages.error(request, 'Пожалуйста, исправьте ошибки.')
    # else:
    #     user_form = UserForm(instance=request.user)
    #     profile_form = ProfileForm(instance=request.user.profile)
    # return render(request, 'profile/index.html', {
    #     'user_form': user_form,
    #     'profile_form': profile_form
    # })

    from allauth.account.views import PasswordChangeView
    from allauth.account.forms import ChangePasswordForm
    from allauth.account.utils import logout_on_password_change

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if request.POST.get('pwd'):
            pwd_form = ChangePasswordForm(data=request.POST, user=request.user)
            if pwd_form.is_valid():
                v = PasswordChangeView.as_view(success_url=reverse_lazy('profile-home'))
                # v.success_url = 'profile-home'
                return v(request)
                # logout_on_password_change(request, pwd_form.user)
                # return redirect('profile-home')
            else:
                messages.error(request, 'Пожалуйста, исправьте ошибки.')
        else:
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'Ваш профиль был успешно обновлен!')
                return redirect('profile-home')
            else:
                messages.error(request, 'Пожалуйста, исправьте ошибки.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        pwd_form = ChangePasswordForm(user=request.user)
    return render(request, 'profile/index.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'pwd_form': pwd_form
    })


def notifies(request):
    notifications = request.user.notifications
    context = {
        'read': notifications.read(),
        'unread': notifications.unread()
    }
    for notify in notifications.unread():
        notify.mark_as_read()

    return render(request, 'profile/notifies.html',context)
