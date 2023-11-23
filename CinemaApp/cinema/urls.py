from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view()),
    path('home/', views.HomeView.as_view(), name = "home"),
    path('login/', views.LoginView.as_view(), name='login'),
    path('sign-up/',views.SignUpView.as_view(),name="sign-up"),
    path('sessions/',views.SessionsView.as_view(),name="sessions"),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('movies/', views.MoviesView.as_view(), name='movies'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('news/', views.NewsView.as_view(), name='news'),
    path('FAQ/', views.FAQView.as_view(), name='FAQ'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('promo/', views.PromoView.as_view(), name='promo'),
    path('vacancy/', views.VacancyView.as_view(), name='vacancy'),
    path('privacy_policy/', views.PrivacyPolicyView.as_view(), name='privacy'),
    path('dashboard/', views.DashBoardsView.as_view(), name='dashboard'),
    path('css/', views.CssView.as_view(), name='css'),

    path('scroll/', views.ScrollView.as_view(), name='scroll'),
    path('custom/', views.CustomView.as_view(), name='custom'),
    path('table/', views.TableView.as_view(), name='table'),
    path('elv/', views.Eleven.as_view(), name='elv'),
    re_path(r'^session/(?P<session_id>\d+)/$', views.SessionView.as_view(), name='session'),
    re_path(r'^movie/(?P<movie_id>\d+)/$', views.MovieView.as_view(), name='movie'),
    re_path(r'^news/(?P<news_id>\d+)/$', views.ArticleView.as_view(), name='article'),
    re_path(r'^ticket_confirmation/(?P<session_id>\d+)_(?P<seat_id>\d+)/$', views.TicketView.as_view(), name='ticket_confirmation'),         
]

