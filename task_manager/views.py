from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import render

User = get_user_model()

def index(request):
    return render(request, 'index.html')

class UserListView(ListView):
    model = User
    template_name = 'users/users_list.html'
    context_object_name = 'users'

class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('login')
    success_message = "Пользователь успешно зарегистрирован!"

class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users_list')
    success_message = "Пользователь успешно обновлен!"

    def test_func(self):
        return self.request.user == self.get_object()

class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('users_list')
    success_message = "Пользователь успешно удален!"

    def test_func(self):
        return self.request.user == self.get_object()

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

class CustomLoginView(SuccessMessageMixin, LoginView):
    template_name = 'registration/login.html'
    success_message = "Вы успешно вошли в систему!"

def custom_logout(request):
    logout(request)
    messages.success(request, "Вы успешно вышли из системы!")
    return redirect('home')