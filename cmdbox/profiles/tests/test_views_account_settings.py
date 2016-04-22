from django.core.urlresolvers import reverse as r
from django.contrib.auth.models import User
from django.test import TestCase

from cmdbox.profiles.forms import UserForm, ProfileForm


class ProfilesAccountSettingsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('john', 'john@doe.com', '123')
        self.client.login(username='john', password='123')
        self.response = self.client.get(r('settings:profile'))

    def test_get(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'profiles/profile.html')

    def test_has_forms(self):
        user_form = self.response.context['user_form']
        profile_form = self.response.context['profile_form']
        self.assertIsInstance(user_form, UserForm)
        self.assertIsInstance(profile_form, ProfileForm)

    def test_html(self):
        self.assertContains(self.response, '<form')
        self.assertContains(self.response, 'type="text"', 4)
        self.assertContains(self.response, 'type="url"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="submit"', 1)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')


class ProfilesAccountSettingsValidPostTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('john', 'john@doe.com', '123')
        self.client.login(username='john', password='123')
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@doe.com',
            'url': 'www.john.com',
            'location': 'Oulu',
            'company': 'John Company'
        }
        self.response = self.client.post(r('settings:profile'), data)

    def test_post(self):
        self.assertEqual(self.response.status_code, 302)

    def test_updated_profile(self):
        user = User.objects.get(username='john')
        self.assertTrue(user.first_name == 'John')
        self.assertTrue(user.profile.location == 'Oulu')


class ProfilesAccountSettingsInvalidPostTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('john', 'john@doe.com', '123')
        self.client.login(username='john', password='123')
        self.response = self.client.post(r('settings:profile'), {'email': 'invalidemail', 'url': 'invalidurl'})

    def test_post(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'profiles/profile.html')

    def test_has_forms(self):
        user_form = self.response.context['user_form']
        profile_form = self.response.context['profile_form']
        self.assertIsInstance(user_form, UserForm)
        self.assertIsInstance(profile_form, ProfileForm)

    def test_form_has_errors(self):
        user_form = self.response.context['user_form']
        profile_form = self.response.context['profile_form']
        self.assertTrue(user_form.errors)
        self.assertTrue(profile_form.errors)
