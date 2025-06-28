from django.contrib import admin
from django.urls import path, include 
from task_manager import views
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
]

urlpatterns += i18n_patterns(
    path('', views.index, name='home'),
    path('users/', views.UserListView.as_view(), name='users_list'),
    path('users/create/', views.UserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/update/', views.UserUpdateView.as_view(), name='user_update'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('statuses/', views.StatusListView.as_view(), name='statuses_list'),
    path('statuses/create/', views.StatusCreateView.as_view(), name='status_create'),
    path('statuses/<int:pk>/update/', views.StatusUpdateView.as_view(), name='status_update'),
    path('statuses/<int:pk>/delete/', views.StatusDeleteView.as_view(), name='status_delete'),
    path('tasks/', views.TaskListView.as_view(), name='tasks_list'),
    path('tasks/create/', views.TaskCreateView.as_view(), name='task_create'),
    path('tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('tasks/<int:pk>/update/', views.TaskUpdateView.as_view(), name='task_update'),
    path('tasks/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    path('labels/', views.LabelListView.as_view(), name='labels_list'),
    path('labels/create/', views.LabelCreateView.as_view(), name='label_create'),
    path('labels/<int:pk>/update/', views.LabelUpdateView.as_view(), name='label_update'),
    path('labels/<int:pk>/delete/', views.LabelDeleteView.as_view(), name='label_delete'),
    path('debug/', views.debug_lang, name='debug_lang'),
)