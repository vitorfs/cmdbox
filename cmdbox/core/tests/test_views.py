from django.core.urlresolvers import reverse as r
from django.contrib.auth.models import User
from django.test import TestCase

from cmdbox.core.forms import SignupForm


class HomeTests(TestCase):
    def setUp(self):
        self.response = self.client.get(r('home'))

    def test_get(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'core/home.html')


class SignUpTests(TestCase):
    def setUp(self):
        self.response = self.client.get(r('signup'))

    def test_get(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'core/signup.html')

    def test_html(self):
        self.assertContains(self.response, '<form')
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)
        self.assertContains(self.response, 'type="submit"', 1)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')


class SignUpValidPostTests(TestCase):
    def setUp(self):
        data = {'username': 'john', 'email': 'john@doe.com', 'password1': '123', 'password2': '123'}
        self.response = self.client.post(r('signup'), data)

    def test_post(self):
        self.assertEqual(self.response.status_code, 302)

    def test_created_user(self):
        self.assertTrue(User.objects.filter(username='john').exists())


class SignUpInvalidPostTests(TestCase):
    def setUp(self):
        self.response = self.client.post(r('signup'), {})

    def test_post(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'core/signup.html')

    def test_has_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, SignupForm)

    def test_form_has_errors(self):
        form = self.response.context['form']
        self.assertTrue(form.errors)
