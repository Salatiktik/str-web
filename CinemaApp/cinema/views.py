import requests
from django.shortcuts import render, redirect
from .forms import LoginForm, SignUpForm
from .models import Session, Movie, Seat, SessionSeat, Genre, News, FAQ, Review, Employee, Add, Promo, RotationSettings
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db.models import Count
import jsonpickle
import datetime
import logging
import plotly.express as px
logging.basicConfig(level=logging.INFO, filename='info.log',filemode='w',format="%(asctime)s| %(message)s")
logging.basicConfig(level=logging.ERROR, filename='error.log',filemode='w',format="%(asctime)s| %(message)s")

class HomeView(View):

    def post(self, req, *args, **kwargs):
        if(not User.objects.get(id=req.user.id).is_superuser):
            return redirect('/home')
        
        r = RotationSettings.objects.get(id=1) 
        r.interval = req.POST.get('brot')
        r.save()
        return redirect('/home')

    def get(self, req, *args, **kwargs):
        
        adds = Add.objects.all()

        newestAddedMovies=Movie.objects.all()[0:3]
        news = (News.objects.all().order_by('date')[::-1])[:3]
        
        reviews = (Review.objects.all().order_by('date')[::-1])[:3]
        sessionsFiltered=[]
        sessions=Session.objects.filter(startDate=datetime.date.today()).order_by('movie','startTime')
        for j in range(len(sessions)):
                if j == 0:
                    sessionsFiltered.append([])
                    sessionsFiltered[0].append(sessions[0])
                    continue
                
                if(sessions[j].movie!=sessions[j-1].movie):
                    sessionsFiltered.append([])
                    sessionsFiltered[len(sessionsFiltered)-1].append(sessions[j])
                    continue

                sessionsFiltered[len(sessionsFiltered)-1].append(sessions[j])

        if(not req.user.is_anonymous):
            is_admin = User.objects.get(id=req.user.id).is_superuser
        else:
            is_admin = False

        return render(req,'cinema/home.html',{"newest":newestAddedMovies,'day':sessionsFiltered,'news':news,'reviews':reviews,'adds':jsonpickle.encode(list(adds)),'is_admin':is_admin,'interval':RotationSettings.objects.get(id=1).interval})

class LoginView(View):
    form_class = LoginForm

    def post(self,req,*args,**kwargs):
        form = self.form_class(data = req.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(req, username=username,password=password)
            logging.info("user {username} try to authenticate".format(username=username))

            if user is not None:
                logging.info('user {0} authenticate'.format(username))
                login(req, user)

                return redirect('/home')
            else:
                logging.error('user {0} authentication error'.format(username))
                return render(req,'registration/login.html',{"form":form, "error":['Wrong username or password']})

    def get(self, req, *args, **kwargs):
        form = self.form_class()
        return render(req,'registration/login.html',{"form":form})


class SignUpView(View):
    form_class = SignUpForm

    def post(self,req,*args,**kwargs):
        form = self.form_class(data = req.POST)
        logout(req)
        if form.is_valid():
            
            user = User.objects.create_user(username=form.cleaned_data["username"],
                                            email=form.cleaned_data["email"],
                                            password=form.cleaned_data["password"])
            logging.info('user {0} created'.format(user.username))
            login(req,user)
            return redirect('/home')
        else:
            logging.error('user {0} authentication error'.format(user.username))            
            return render(req,'registration/sign_up.html',{"form":form,"error":form.errors.values})


    def get(self, req, *args, **kwargs):
        form = self.form_class()
        return render(req,'registration/sign_up.html',{"form":form})

class SessionsView(View):
    date = datetime.date.today()+datetime.timedelta(days=8)
    def get(self, req, *args, **kwargs):
        GET = req.GET.copy()
        sessions = []
        sessionsFiltered = []
        context={}
        
        if(req.GET.get('date','')!=''):
            print('date')
            context['date']=req.GET.get('date')
            sessions=Session.objects.filter(startDate__gte=req.GET.get('date'),
                                            startDate__lte=req.GET.get('date')).order_by('movie','startTime')
            for j in range(len(sessions)):
                    if j == 0:
                        sessionsFiltered.append([])
                        sessionsFiltered[0].append(sessions[0])
                        continue
                    
                    if(sessions[j].movie!=sessions[j-1].movie):
                        sessionsFiltered.append([])
                        sessionsFiltered[len(sessionsFiltered)-1].append(sessions[j])
                        continue

                    sessionsFiltered[len(sessionsFiltered)-1].append(sessions[j])

            sessionsFiltered = [sessionsFiltered]
            
        else:
            for i in range(7):
                sessions.append(Session.objects.filter(startDate__gte=datetime.date.today()+datetime.timedelta(days=i),
                                            startDate__lte=datetime.date.today()+datetime.timedelta(days=i)).order_by('movie','startTime'))
                sessionsFiltered.append([])
                for j in range(len(sessions[i])):
                    if j == 0:
                        sessionsFiltered[i].append([])
                        sessionsFiltered[i][0].append(sessions[i][0])
                        continue
                    
                    if(sessions[i][j].movie!=sessions[i][j-1].movie):
                        sessionsFiltered[i].append([])
                        sessionsFiltered[i][len(sessionsFiltered[i])-1].append(sessions[i][j])
                        continue

                    sessionsFiltered[i][len(sessionsFiltered[i])-1].append(sessions[i][j])
            
        if(req.GET.get('pfrom','')!=''):
            context['pfrom']=req.GET.get('pfrom')
            for i in range(len(sessionsFiltered)):
                for j in range(len(sessionsFiltered[i])):
                    sessionsFiltered[i][j]=list(filter(lambda x: x.price>=float(req.GET.get('pfrom')),sessionsFiltered[i][j]))
        
        if(req.GET.get('pto','')!=''):
            context['pto']=req.GET.get('pto')
            for i in range(len(sessionsFiltered)):
                for j in range(len(sessionsFiltered[i])):
                    sessionsFiltered[i][j]=list(filter(lambda x: x.price<=float(req.GET.get('pto')),sessionsFiltered[i][j]))

        if(req.GET.get('format2D','')!=''):
            context['format2D']=True
            for i in range(len(sessionsFiltered)):
                for j in range(len(sessionsFiltered[i])):
                    sessionsFiltered[i][j]=list(filter(lambda x: x.type=='2D',sessionsFiltered[i][j]))

        if(req.GET.get('format3D','')!=''):
            context['format3D']=True
            for i in range(len(sessionsFiltered)):
                for j in range(len(sessionsFiltered[i])):
                    sessionsFiltered[i][j]=list(filter(lambda x: x.type=='3D',sessionsFiltered[i][j]))

        context['sessions']=sessionsFiltered

        return render(req,'cinema/sessions.html',context)
    
class SessionView(View):
    def get(self, req, *args,session_id, **kwargs):
        if req.user.is_anonymous:
            return redirect('/login')
        session = Session.objects.get(id=session_id)
        hall = session.hall
        seats = Seat.objects.filter(hall=hall).order_by('number','row')
        sessionSeats = []
        seatsClear = [[] for x in range(seats[len(seats)-1].row)]
        for i in range(len(seats)):
            if(SessionSeat.objects.filter(session=session,seat=seats[i])):
                sessionSeats.append(SessionSeat.objects.get(session=session,seat=seats[i]))
                seatsClear[seats[i].row-1].append(sessionSeats[len(sessionSeats)-1])
                continue


            seatsClear[seats[i].row-1].append(seats[i])

        movie = session.movie
        return render(req,'cinema/session.html',{"session":session,"hall":hall,"seats":seatsClear,"sessionSeats":sessionSeats,"movie":movie,"posterUrl":movie.poster.url})
    
class MovieView(View):
    def post(self, req, *args, movie_id, **kwargs):
        Review.objects.create(movie=Movie.objects.get(id=movie_id),author=req.user,date=datetime.date.today(),text=req.POST.get('text'),rate=req.POST.get('rating'))
        return redirect('/movie/{0}'.format(movie_id))

    def get(self, req, *args, movie_id, **kwargs):
        movie = Movie.objects.get(id=movie_id)
        rating=0
        reviews=Review.objects.filter(movie=movie_id)
        for review in reviews:
            rating+=review.rate

        if(len(reviews)!=0):
            rating=round(rating/len(reviews),1)
        sessions = []
        for i in range(7):
            sessions.append(Session.objects.filter(movie = movie, startDate__gte=datetime.date.today()+datetime.timedelta(days=i+1),
                                          startDate__lt=datetime.date.today()+datetime.timedelta(days=i+2)))

        return render(req, 'cinema/movie.html', {"movie":movie, "rating":rating, "sessions":sessions,'reviews':reviews})

class MoviesView(View):
    def get(self, req, *args, **kwargs):
        movies = Movie.objects.filter(rating__gte=float(req.GET.get('rfrom','0')) if req.GET.get('rfrom')!='' else 0,
                                      rating__lt=float(req.GET.get('rto','10')) if req.GET.get('rto')!='' else 10)
        genres = Genre.objects.all()
        
        if(len(req.GET)>2):
            genre_filter=[]
            for genre in genres:
                if(req.GET.get(str(genre)+'checkbox')):
                    genre_filter.append(genre)

            movies = movies.filter(genre__in=genre_filter).distinct()

            return render(req, 'cinema/movies.html',{"movies":movies,'genres':genres,'genreFilter':genre_filter})
        
        return render(req, 'cinema/movies.html',{"movies":movies,'genres':genres})

class TicketView(View):

    def post(self,req,*args, session_id, seat_id,**kwargs):
        SessionSeat.objects.create(seat = Seat.objects.get(id=seat_id),finall_cost = req.POST.get('costIn') ,session=Session.objects.get(id=session_id), is_occupied = True, user = self.request.user)
        logging.info('user {0} buy ticket'.format(self.request.user.username))
        return redirect(('/home'))

    def get(self, req, *args, session_id, seat_id, **kwargs):
        if req.user.is_anonymous:
            return redirect('/login')
        
        promocode = Promo.objects.all()

        self.seat_id = seat_id
        self.session_id = session_id
        session = Session.objects.get(id=session_id)
        seat = Seat.objects.get(id=seat_id)
        qr = requests.get("https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=seat{0}session{1}&color=5fa278&bgcolor=97edb6".format(seat_id,session_id))
        return render(req,'cinema/ticket.html',{"session":session,"seat":seat,"qr":qr,'cost':seat.type.rate*session.price,'promo':jsonpickle.encode(list(promocode))})
    
class ProfileView(View):
    def get(self, req, *args, **kwargs):
        if req.user.is_anonymous:
            return redirect('/login')
        
        tickets = SessionSeat.objects.filter(user=self.request.user)
        return render(req,'cinema/profile.html',{"tickets":tickets})
    
class NewsView(View):
    def get(self,req,*args,**kwargs):
        news = News.objects.all().order_by('date')[::-1]
        return render(req,'cinema/news.html',{'news':news})

class ArticleView(View):
    def get(self,req,*args,**kwargs):
        article = News.objects.get(id=kwargs['news_id'])
        return render(req,'cinema/article.html',{'article':article})

class AboutView(View):
    def get(self,req,*args,**kwargs):
        return render(req,'cinema/about.html',{})
    
class ScrollView(View):
    def get(self,req,*args,**kwargs):
        return render(req,'cinema/scroll.html',{})

class CustomView(View):
    def get(self,req,*args,**kwargs):
        return render(req,'cinema/custom.html',{})

class TableView(View):
    def get(self,req,*args,**kwargs):
        return render(req,'cinema/table.html',{})


class FAQView(View):
    def get(self, req, *args, **kwargs):
        faq = FAQ.objects.all().order_by('date')[::-1]
        return render(req, 'cinema/faq.html',{'faq':faq})
    
class ContactsView(View):
    def get(self, req, *args, **kwargs):
        contacts = Employee.objects.all()
        return render(req, 'cinema/contacts.html',{"contacts":contacts})
    
class VacancyView(View):
    def get(self, req, *args, **kwargs):
        return render(req, 'cinema/vacancy.html',{})
    
class PrivacyPolicyView(View):
    def get(self, req, *args, **kwargs):
        return render(req, 'cinema/privacy.html',{})

class PromoView(View):
    def get(self, req, *args, **kwargs):
        return render(req, 'cinema/promo.html',{})
    
class DashBoardsView(View):
    def get(self, req, *args, **kwargs):
        if(not User.objects.get(id=req.user.id).is_superuser):
            return redirect('/home')
        tickets_day = {}
        tickets_movie= {}
        tickets = SessionSeat.objects.values('session').annotate(tcount=Count('session')).order_by('session')
        for i in tickets:
            if(tickets_day.get(str(Session.objects.get(id=i['session']).startDate),0)==0):
                tickets_day[str(Session.objects.get(id=i['session']).startDate)]=i['tcount']
            else:
                tickets_day[str(Session.objects.get(id=i['session']).startDate)]+=i['tcount']

            if(tickets_movie.get(str(Session.objects.get(id=i['session']).movie),0)==0):
                tickets_movie[str(Session.objects.get(id=i['session']).movie)]=i['tcount']
            else:
                tickets_movie[str(Session.objects.get(id=i['session']).movie)]+=i['tcount']

        au=len(User.objects.all())
        at=len(SessionSeat.objects.all())
        ass=len(Session.objects.all())
        am=len(Movie.objects.all())
        tickets = SessionSeat.objects.all()
        mg = 0
        for i in tickets:
            mg+=round(i.session.price*i.seat.type.rate,2)

        td = px.bar(
            x=tickets_day.keys(),
            y=tickets_day.values(),
            title="Amount of tickets in day",
            labels={'x':'Date','y':'tickets amount'}
        )

        tm = px.bar(
            x=tickets_movie.keys(),
            y=tickets_movie.values(),
            title="Amount of tickets for movie",
            labels={'x':'Movies','y':'tickets amount'}
        )

        return render(req, 'cinema/dash.html',{'td':td.to_html(),'tm':tm.to_html(),'au':au,'at':at,'am':am,'ass':ass,'mg':mg})

class CssView(View):
    def get(self, req, *args, **kwargs):
        return render(req, 'cinema/cssDock.html',{})
      
class Eleven(View):
    def get(self, req, *args, **kwargs):
        return render(req, 'cinema/eleven.html',{})
