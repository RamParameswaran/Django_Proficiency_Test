import pytest
from django.test import RequestFactory, TestCase, Client

from .factories import UserFactory

from django_proficiency_test.users.models import User
from django_proficiency_test.users.views import UserRedirectView, UserUpdateView

pytestmark = pytest.mark.django_db


class TestUserUpdateView:
    """
    TODO:
        extracting view initialization code as class-scoped fixture
        would be great if only pytest-django supported non-function-scoped
        fixture db access -- this is a work-in-progress for now:
        https://github.com/pytest-dev/pytest-django/pull/258
    """

    def test_get_success_url(self, user: User, request_factory: RequestFactory):
        view = UserUpdateView()
        request = request_factory.get("/fake-url/")
        request.user = user

        view.request = request

        assert view.get_success_url() == f"/users/{user.username}/"

    def test_get_object(self, user: User, request_factory: RequestFactory):
        view = UserUpdateView()
        request = request_factory.get("/fake-url/")
        request.user = user

        view.request = request

        assert view.get_object() == user


class TestUserRedirectView:
    def test_get_redirect_url(self, user: User, request_factory: RequestFactory):
        view = UserRedirectView()
        request = request_factory.get("/fake-url")
        request.user = user

        view.request = request

        assert view.get_redirect_url() == f"/users/{user.username}/"


class TestUserCreation(TestCase):
    def test_create_user(self):

        user = UserFactory()
        c = Client()
        response = c.post(
            "/accounts/signup/", {'email': user.email, 'username': user.username, 'password1': user.password, 'password2': user.password})

        assert response.status_code == 200

    def test_duplicate_email_fails(self):
        import xhtml2pdf

        user = UserFactory()
        c = Client()
        response = c.post(
            "/accounts/signup/", {'email': user.email, 'username': user.username, 'password1': user.password, 'password2': user.password})

        print(User.objects.all())

        cb = Client()
        response2 = cb.post(
            "/accounts/signup/", {'email': user.email, 'username': user.username, 'password1': user.password, 'password2': user.password})

        assert len(User.objects.all()) == 1
        assert response2.status_code == 404
