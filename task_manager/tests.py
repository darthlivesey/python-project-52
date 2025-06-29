from django.test import TestCase
from .models import Status, Task, Label
from django.test import Client, override_settings
from django.urls import reverse
from django.utils.translation import activate
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm
from django.conf import settings
from django.utils import translation


User = get_user_model()


class BaseTestCase(TestCase):
    def setUp(self):
        super().setUp()
        translation.activate('en')

    def tearDown(self):
        translation.deactivate()
        super().tearDown()


class LocalizationTest(BaseTestCase):
    def test_russian_translation(self):
        current_language = translation.get_language()
        translation.activate('ru')
        from django.utils.translation import gettext as _
        try:
            self.assertEqual(_("Task Manager"), "Менеджер задач")
        finally:
            translation.activate(current_language)


class UserViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
            email='test@example.com'
        )

    def test_user_list_view(self):
        response = self.client.get(reverse('users_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')

    def test_user_create_view(self):
        response = self.client.post(reverse('user_create'), {
            'username': 'newuser',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
            'email': 'new@example.com'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_update_view(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(reverse('user_update', args=[self.user.pk]), {
            'username': 'updateduser',
            'first_name': 'Updated',
            'last_name': 'User',
            'email': 'updated@example.com'
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')

    def test_user_delete_view(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(reverse('user_delete', args=[self.user.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())

    def test_login_view(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertFalse('_auth_user_id' in self.client.session)


class StatusViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.status = Status.objects.create(name='Test Status')

    def test_status_list_requires_login(self):
        response = self.client.get(reverse('statuses_list'))
        self.assertRedirects(
            response,
            f'/{settings.LANGUAGE_CODE}/login/?next=/{settings.LANGUAGE_CODE}/statuses/'
        )

    def test_status_create(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('status_create'), {'name': 'New Status'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name='New Status').exists())

    def test_status_update(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(
            reverse('status_update', args=[self.status.pk]),
            {'name': 'Updated Status'}
        )
        self.assertEqual(response.status_code, 302)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Updated Status')

    def test_status_delete(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('status_delete', args=[self.status.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Status.objects.filter(pk=self.status.pk).exists())

    def test_status_delete_protected(self):
        Task.objects.create(
            name='Protected Task',
            description='Task using status',
            status=self.status,
            creator=self.user
        )

        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('status_delete', args=[self.status.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(pk=self.status.pk).exists())
        self.assertIn(
            "Невозможно удалить статус, используемый в задачах",
            [msg.message for msg in response.wsgi_request._messages]
        )


class TaskViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.status = Status.objects.create(name='Test Status')
        self.task = Task.objects.create(
            name='Test Task',
            description='Test Description',
            status=self.status,
            creator=self.user
        )

    def test_task_list_requires_login(self):
        response = self.client.get(reverse('tasks_list'))
        self.assertRedirects(
            response,
            f'/{settings.LANGUAGE_CODE}/login/?next=/{settings.LANGUAGE_CODE}/tasks/'
        )

    def test_task_create(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('task_create'), {
            'name': 'New Task',
            'description': 'New Description',
            'status': self.status.pk,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name='New Task').exists())

    def test_task_update(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(
            reverse('task_update', args=[self.task.pk]),
            {
                'name': 'Updated Task',
                'description': 'Updated Description',
                'status': self.status.pk,
                'executor': self.user.pk,
            }
        )
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Updated Task')

    def test_task_delete(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('task_delete', args=[self.task.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_task_delete_only_by_creator(self):
        User.objects.create_user(username='anotheruser', password='testpass')
        self.client.login(username='anotheruser', password='testpass')
        response = self.client.post(reverse('task_delete', args=[self.task.pk]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())


class LabelViewsTest(BaseTestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.label = Label.objects.create(name='Test Label', creator=self.user)
        self.task = Task.objects.create(
            name='Test Task',
            description='Test Description',
            status=Status.objects.create(name='Test Status'),
            creator=self.user
        )

    def test_label_list_requires_login(self):
        response = self.client.get(reverse('labels_list'))
        self.assertRedirects(
            response,
            f'/{settings.LANGUAGE_CODE}/login/?next=/{settings.LANGUAGE_CODE}/labels/'
        )

    def test_label_create(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('label_create'), {'name': 'New Label'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(name='New Label').exists())

    def test_label_delete_protected(self):
        self.task.labels.add(self.label)
        self.client.login(username='testuser', password='testpass')
        self.client.post(reverse('label_delete', args=[self.label.pk]))
        self.assertTrue(Label.objects.filter(pk=self.label.pk).exists())

    def test_task_create_with_labels(self):
        self.client.login(username='testuser', password='testpass')
        label = Label.objects.create(name='Bug', creator=self.user)
        response = self.client.post(reverse('task_create'), {
            'name': 'New Task',
            'description': 'Test Description',
            'status': Status.objects.first().pk,
            'labels': [label.id]
        })
        self.assertEqual(response.status_code, 302)
        task = Task.objects.get(name='New Task')
        self.assertEqual(task.labels.count(), 1)

    def test_label_delete_allowed(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('label_delete', args=[self.label.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Label.objects.filter(pk=self.label.pk).exists())

    def test_label_update(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(
            reverse('label_update', args=[self.label.pk]),
            {'name': 'Updated Label'}
        )
        self.assertEqual(response.status_code, 302)
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'Updated Label')

    def test_label_create_invalid(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('label_create'), {'name': ''})
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context)
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn('name', form.errors)
        self.assertEqual(
            form.errors['name'][0],
            'This field is required.'
        )

    def test_label_delete_no_permission(self):
        User.objects.create_user(username='another', password='testpass')
        self.client.login(username='another', password='testpass')
        response = self.client.post(reverse('label_delete', args=[self.label.pk]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Label.objects.filter(pk=self.label.pk).exists())


class TaskFilterTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='testpass'
        )

        self.status1 = Status.objects.create(name='Status1')
        self.status2 = Status.objects.create(name='Status2')

        self.label1 = Label.objects.create(name='Label1', creator=self.user)
        self.label2 = Label.objects.create(name='Label2', creator=self.user)

        self.task1 = Task.objects.create(
            name='Task with Status1',
            status=self.status1,
            creator=self.user,
            executor=self.user
        )
        self.task1.labels.add(self.label1)

        self.task2 = Task.objects.create(
            name='Task with Status2',
            status=self.status2,
            creator=self.user,
            executor=self.other_user
        )
        self.task2.labels.add(self.label2)

        self.task3 = Task.objects.create(
            name='Other user task',
            status=self.status1,
            creator=self.other_user,
            executor=self.user
        )

        self.client.login(username='testuser', password='testpass')

    def test_filter_by_status(self):
        response = self.client.get(
            reverse('tasks_list') + f'?status={self.status1.id}'
        )
        self.assertContains(response, self.task1.name)
        self.assertContains(response, self.task3.name)
        self.assertNotContains(response, self.task2.name)

    def test_filter_by_executor(self):
        response = self.client.get(
            reverse('tasks_list') + f'?executor={self.other_user.id}'
        )
        self.assertContains(response, self.task2.name)
        self.assertNotContains(response, self.task1.name)
        self.assertNotContains(response, self.task3.name)

    def test_filter_by_labels(self):
        response = self.client.get(
            reverse('tasks_list') + f'?labels={self.label1.id}'
        )
        self.assertContains(response, self.task1.name)
        self.assertNotContains(response, self.task2.name)
        self.assertNotContains(response, self.task3.name)

    def test_filter_self_tasks(self):
        response = self.client.get(
            reverse('tasks_list') + '?self_tasks=on'
        )
        self.assertContains(response, self.task1.name)
        self.assertContains(response, self.task2.name)
        self.assertNotContains(response, self.task3.name)

    def test_combined_filters(self):
        response = self.client.get(
            reverse('tasks_list')
            + f'?status={self.status1.id}&self_tasks=on'
        )
        self.assertContains(response, self.task1.name)
        self.assertNotContains(response, self.task2.name)
        self.assertNotContains(response, self.task3.name)
