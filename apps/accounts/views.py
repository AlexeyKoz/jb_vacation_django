from django.shortcuts import render
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import UserCreationForm, UserChangeForm

# Create your views here.


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        messages.success(
            self.request, 'Account created successfully! Please log in.')
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, UpdateView):
    form_class = UserChangeForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)
