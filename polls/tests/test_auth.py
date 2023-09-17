from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthenticationTestCase(TestCase):
    def setUp(self):
        """
        Set up a test user for authentication-related tests.
        """
        self.test_user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )

    def test_signup_view(self):
        """
        Test the signup view for a successful response and template usage.
        """
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")

    def test_signup_form_invalid(self):
        """
        Test the signup form with invalid data and check for error messages.
        """
        response = self.client.post(reverse("signup"), {
                                    "username": "testuser", "password1": "password", "password2": "password"})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, "form", "username",
                             "A user with that username already exists.")

    def test_login_view(self):
        """
        Test the login view for a successful response and template usage.
        """
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_login_invalid_user(self):
        """
        Test login with invalid user credentials and check for error message.
        """
        response = self.client.post(
            reverse("login"), {"username": "nonexistentuser", "password": "wrongpassword"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "Please enter a correct username and password.")

    def test_logout_view(self):
        """
        Test the logout view for a successful redirection.
        """
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("polls:index"))

    def test_vote_authenticated_user(self):
        """
        Test voting for an authenticated user with a GET request.
        """
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("polls:vote", args=(1,)))
        self.assertEqual(response.status_code, 404)

    def test_vote_unauthenticated_user(self):
        """
        Test voting for an unauthenticated user with a GET request.
        """
        response = self.client.get(reverse("polls:vote", args=(1,)))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f"{reverse('login')}?next={reverse('polls:vote', args=(1,))}")

    def test_vote_authenticated_user_post(self):
        """
        Test voting for an authenticated user with a POST request.
        """
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("polls:vote", args=(1,)), {"choice": 1})
        self.assertEqual(response.status_code, 404)

    def test_vote_unauthenticated_user_post(self):
        """
        Test voting for an unauthenticated user with a POST request.
        """
        response = self.client.post(
            reverse("polls:vote", args=(1,)), {"choice": 1})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f"{reverse('login')}?next={reverse('polls:vote', args=(1,))}")

    def test_logout_authenticated_user(self):
        """
        Test logout for an authenticated user.
        """
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("polls:index"))

    def test_logout_unauthenticated_user(self):
        """
        Test logout for an unauthenticated user.
        """
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("polls:index"))
