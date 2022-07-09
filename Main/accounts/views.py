from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect
from .forms import NewUSerForm, EditUserForm, EditProfileForm
from django.views.generic import TemplateView, DetailView, View, ListView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, update_session_auth_hash
from .models import Userprofile
from django.utils import timezone

# Create your views here.

def signup_view(request):
    if request.method == 'POST':
        form = NewUSerForm(request.POST)
        if form.is_valid():
            user = form.save()
            Userprofile.objects.create(user=user)
            return redirect('food:home')
    else:
        form = NewUSerForm()

    context = {
        'form': form
    }
    return render(request, 'registrations/signup.html', context)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('food:home')
    else:
        form = PasswordChangeForm(data=request.POST, user=request.user)

    context = {
        'form': form
    }
    return render(request, 'registrations/change_password.html', context)


class UserDetailView(DetailView):
    model = User
    template_name = "registrations/user_detail.html"

def user_edit(request, pk):
    d_user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = EditUserForm(request.POST, instance=d_user)
        if form.is_valid:
            user = form.save(commit=False)
            user.user = request.user
            user.save()
            return redirect('account:user_detail', pk=user.pk)
        form = EditUserForm()
    else:
        form = EditUserForm(instance=d_user)

    context = {
        'form': form
    }
    return render(request, 'registrations/user_edit.html', context)


def profile_edit(request, pk):
    user_profile = get_object_or_404(Userprofile, pk=pk)
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=user_profile)
        if form.is_valid:
            user = form.save(commit=False)
            user.user = request.user
            user.created_date = timezone.now()
            user.save()
            return redirect('account:user_detail', pk=user.pk)
        form = EditProfileForm()
    else:
        form = EditProfileForm(instance=user_profile)

    context = {
        'form': form
    }
    return render(request, 'registrations/profile_edit.html', context)