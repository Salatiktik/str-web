from django.test import SimpleTestCase
from django.urls import reverse, resolve
from cinema.views import HomeView,LoginView,SignUpView,SessionsView,ProfileView,MoviesView,MovieView,SessionView,TicketView

class TestUrls(SimpleTestCase):

    def test_home_url_is_resolved(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func.__dict__,HomeView.as_view().__dict__)

    def test_login_url_is_resolved(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func.__dict__,LoginView.as_view().__dict__)

    def test_signup_url_is_resolved(self):
        url = reverse('sign-up')
        self.assertEquals(resolve(url).func.__dict__,SignUpView.as_view().__dict__)

    def test_sessions_url_is_resolved(self):
        url = reverse('sessions')
        self.assertEquals(resolve(url).func.__dict__,SessionsView.as_view().__dict__)

    def test_profile_url_is_resolved(self):
        url = reverse('profile')
        self.assertEquals(resolve(url).func.__dict__,ProfileView.as_view().__dict__)

    def test_movies_url_is_resolved(self):
        url = reverse('movies')
        self.assertEquals(resolve(url).func.__dict__,MoviesView.as_view().__dict__)

    def test_some_movie_url_is_resolved(self):
        url = reverse('movie',args=[1])
        self.assertEquals(resolve(url).func.__dict__,MovieView.as_view().__dict__)

    def test_some_session_url_is_resolved(self):
        url = reverse('session',args=[1])
        self.assertEquals(resolve(url).func.__dict__,SessionView.as_view().__dict__)

    def test_some_ticket_url_is_resolved(self):
        url = reverse('ticket_confirmation',args=[1,1])
        self.assertEquals(resolve(url).func.__dict__,TicketView.as_view().__dict__)