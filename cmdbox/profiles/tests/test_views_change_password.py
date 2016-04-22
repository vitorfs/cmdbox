from django.core.urlresolvers import reverse as r
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.test import TestCase


class ProfilesChangePasswordTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('john', 'john@doe.com', '123')
        self.client.login(username='john', password='123')
        self.response = self.client.get(r('settings:password'))

    def test_get(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'profiles/change_password.html')

    def test_has_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, PasswordChangeForm)

    def test_html(self):
        self.assertContains(self.response, '<form')
        self.assertContains(self.response, 'type="password"', 3)
        self.assertContains(self.response, 'type="submit"', 1)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')


class ProfilesChangePasswordValidPostTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('john', 'john@doe.com', '123')
        self.client.login(username='john', password='123')
        data = {
            'old_password': '123',
            'new_password1': '321',
            'new_password2': '321'
        }
        self.response = self.client.post(r('settings:password'), data)

    def test_post(self):
        self.assertEqual(self.response.status_code, 302)

    def test_changed_password(self):
        self.assertTrue(self.client.login(username='john', password='321'))


class ProfilesChangePasswordInvalidPostTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('john', 'john@doe.com', '123')
        self.client.login(username='john', password='123')
        self.response = self.client.post(r('settings:password'), dict())

    def test_post(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'profiles/change_password.html')

    def test_has_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, PasswordChangeForm)

    def test_form_has_errors(self):
        form = self.response.context['form']
        self.assertTrue(form.errors)
