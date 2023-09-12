from django.test import TestCase, Client
from django.urls import reverse
from django.core.management import call_command
from django.contrib.auth.models import User


class TestViews(TestCase):
    def setUpTestData():
        call_command('loaddata','cinema_testdata1.json')

    def setUp(self):
         self.client = Client()

    def test_home_GET(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'cinema/home.html')
        self.assertTemplateUsed(response,'cinema/base.html')

    def test_login_GET(self):
        response = self.client.get(reverse('login'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'registration/login.html')
        self.assertTemplateUsed(response,'cinema/base.html')

    def test_login_POST_valid_user(self):
        User.objects.create_user(username='valid',password='valid')

        response = self.client.post(reverse('login'),{
            'username': 'valid',
            'password': 'valid'
        })

        self.assertEqual(response.status_code, 302)
        
    def test_login_POST_invalid_user(self):
        User.objects.create_user(username='valid',password='valid')

        response = self.client.post(reverse('login'),{
            'username': 'invalid',
            'password': 'invalid'
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'registration/login.html')
        self.assertTemplateUsed(response,'cinema/base.html')

    def test_signup_GET(self):
        response = self.client.get(reverse('sign-up'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'registration/sign_up.html')
        self.assertTemplateUsed(response,'cinema/base.html')

    def test_signup_POST_valid_form(self):
        response = self.client.post(reverse('sign-up'),{
            'username':'valid',
            'email':'valid@valid.com',
            'password':'validpassword123',
            'passwordConfirm':'validpassword123'
        })

        user=User.objects.get(username='valid')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(user.email, 'valid@valid.com')

    def test_signup_POST_invalid_form(self):
        response = self.client.post(reverse('sign-up'),{
            'username':'invalid',
            'password':'invalidpassword123',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'registration/sign_up.html')
        self.assertTemplateUsed(response,'cinema/base.html')

    def test_Sessions_GET_default(self):
        response = self.client.get(reverse('sessions'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'cinema/sessions.html')
        self.assertTemplateUsed(response,'cinema/base.html')

    def test_Sessions_GET_filtered(self):
        response = self.client.get(reverse('sessions'),{
            'date':'0001-01-01',
            'pfrom':'1',
            'pto':'2',
            'format2D':'on'
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'cinema/sessions.html')
        self.assertTemplateUsed(response,'cinema/base.html')

    def test_Session_GET_unauth(self):
        response = self.client.get(reverse('session',args=[1]))

        self.assertEqual(response.status_code, 302)
        
    def test_Session_GET_auth(self):
        User.objects.create_user(username='valid',password='valid')
        self.client.login(username='valid',password='valid')
        response = self.client.get(reverse('session',args=[1]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'cinema/session.html')
        self.assertTemplateUsed(response,'cinema/base.html')

    def test_Movie_GET(self):
        response = self.client.get(reverse('movie',args=[1]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'cinema/movie.html')
        self.assertTemplateUsed(response,'cinema/base.html')

    def test_Movies_GET_default(self):
        response = self.client.get(reverse('movies'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'cinema/movies.html')
        self.assertTemplateUsed(response,'cinema/base.html')

    def test_Movies_GET_filtered(self):
        response = self.client.get(reverse('movies'),{
            'rfrom':'5',
            'rto':'8',
            'Dramacheckbox':'on',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'cinema/movies.html')
        self.assertTemplateUsed(response,'cinema/base.html')

    def test_Movie_GET_filtered(self):
        response = self.client.get(reverse('movies'),{
            'rfrom':'5',
            'rto':'8',
            'Dramacheckbox':'on',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'cinema/movies.html')
        self.assertTemplateUsed(response,'cinema/base.html')

    def test_Ticket_GET_unauth(self):
        response = self.client.get(reverse('ticket_confirmation',args=[1,1]))

        self.assertEqual(response.status_code, 302)

    def test_Ticket_GET_auth(self):
        User.objects.create_user(username='valid',password='valid')
        self.client.login(username='valid',password='valid')
        response = self.client.get(reverse('ticket_confirmation',args=[1,1]))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'cinema/ticket.html')
        self.assertTemplateUsed(response,'cinema/base.html')

    def test_Ticket_POST(self):
        User.objects.create_user(username='valid',password='valid')
        self.client.login(username='valid',password='valid')
        response = self.client.post(reverse('ticket_confirmation',args=[1,1]))
        
        self.assertEqual(response.status_code, 302)

    def test_Profile_GET_unauth(self):
        response = self.client.get(reverse('profile'))

        self.assertEqual(response.status_code, 302)

    def test_Profile_GET_auth(self):
        User.objects.create_user(username='valid',password='valid')
        self.client.login(username='valid',password='valid')
        response = self.client.get(reverse('profile'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'cinema/profile.html')
        self.assertTemplateUsed(response,'cinema/base.html')