from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.conf import settings
from django.shortcuts import redirect
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import render
from .models import Status, Task, Label
from .forms import StatusForm, TaskForm, LabelForm
from django.utils.translation import gettext as _
from django_filters.views import FilterView
from .filters import TaskFilter


User = get_user_model()


def debug_lang(request):
    from django.utils import translation
    info = {
        "REQUEST_LANGUAGE": request.LANGUAGE_CODE,
        "GET_LANGUAGE": translation.get_language(),
        "SESSION_LANGUAGE": request.session.get('django_language', 'not set'),
        "COOKIE_LANGUAGE": request.COOKIES.get('django_language', 'not set'),
        "LOCALE_PATHS": settings.LOCALE_PATHS,
    }
    return render(request, 'debug.html', {'info': info})


def index(request):
    return render(request, 'index.html')


class StatusListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = Status
    template_name = 'statuses/statuses_list.html'
    context_object_name = 'statuses'


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _("Статус успешно создан")


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _("Статус успешно изменен")


class StatusDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'statuses/status_confirm_delete.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _("Статус успешно удален")

    def post(self, request, *args, **kwargs):
        status = self.get_object()
        if status.task_set.exists():
            messages.error(request, _("Невозможно удалить статус, используемый в задачах"))
            return redirect('statuses_list')
        return super().post(request, *args, **kwargs)


class UserListView(ListView):
    model = User
    template_name = 'users/users_list.html'
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('login')
    success_message = _("Пользователь успешно зарегистрирован!")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = _("Create user")
        return context


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users_list')
    success_message = _("Пользователь успешно обновлен!")

    def test_func(self):
        return self.request.user == self.get_object()


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('users_list')
    success_message = _("Пользователь успешно удален!")

    def test_func(self):
        return self.request.user == self.get_object()

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class CustomLoginView(SuccessMessageMixin, LoginView):
    template_name = 'registration/login.html'
    success_message = _("Вы успешно вошли в систему!")


def custom_logout(request):
    logout(request)
    messages.success(request, _("Вы успешно вышли из системы!"))
    return redirect('home')


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks_list')
    success_message = _("Задача успешно создана")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        response = super().form_valid(form)
        return response


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks_list')
    success_message = _("Задача успешно изменена")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        response = super().form_valid(form)
        return response


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('tasks_list')
    success_message = _("Задача успешно удалена")

    def test_func(self):
        return self.request.user == self.get_object().creator


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/label_list.html'
    context_object_name = 'labels'


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/label_form.html'
    success_url = reverse_lazy('labels_list')
    success_message = _("Метка успешно создана")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/label_form.html'
    success_url = reverse_lazy('labels_list')
    success_message = _("Метка успешно изменена")


class LabelDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'labels/label_confirm_delete.html'
    success_url = reverse_lazy('labels_list')
    success_message = _("Метка успешно удалена")

    def test_func(self):
        return self.request.user == self.get_object().creator

    def post(self, request, *args, **kwargs):
        label = self.get_object()
        if label.tasks.exists():
            messages.error(request, _("Невозможно удалить метку, используемую в задачах"))
            return redirect('labels_list')
        return super().post(request, *args, **kwargs)


class TaskListView(LoginRequiredMixin, FilterView):
    model = Task
    filterset_class = TaskFilter
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 10

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        kwargs['request'] = self.request
        return kwargs
