from django.db import models
from django.contrib.auth import get_user_model
import re

# Create your models here.

User = get_user_model()

class Genre(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name

class Movie(models.Model):
    name = models.CharField(max_length=30)
    country = models.CharField(max_length=20)
    genre = models.ManyToManyField(Genre, related_name="movie")
    duration = models.TimeField()
    budget = models.FloatField()
    poster = models.ImageField()
    description = models.CharField(max_length=1000)
    rating = models.FloatField()
    trailerUrl = models.CharField(max_length=50)

    @property
    def trailerId(self):
        regEx = r"^.*((youtu\.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*"
        match = re.search(regEx,self.trailerUrl)
        return match.group(7)

    def __str__(self):
        return self.name


class Hall(models.Model):
    name = models.CharField(max_length=30)
    capacity = models.IntegerField()
    type = models.CharField(
        max_length=30,
        choices=(
            ('default', 'default'),
            ('IMAX', 'IMAX'),
        )
    )
    
    def __str__(self):
        return self.name


class SeatType(models.Model):
    type = models.CharField(max_length=10)
    rate = models.FloatField()
    
    def __str__(self):
        return self.type


class Seat(models.Model):
    hall = models.ForeignKey(
        Hall,
        on_delete=models.CASCADE,
        related_name="seats"
    )
    row = models.IntegerField()
    number = models.IntegerField()
    type = models.ForeignKey(
        SeatType, 
        on_delete=models.CASCADE, 
        related_name="types"
    )

    def __str__(self):
        return f"row {self.row} place {self.number}"

class Session(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    startTime = models.TimeField()
    startDate = models.DateField()
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    price = models.FloatField()
    type = models.CharField(
        max_length=30,
        choices=(
            ('3D', '3D'),
            ('2D', '2D'),
        )
    )

    def __str__(self):
        return f"{self.movie.__str__()}:{self.startTime}"


class SessionSeat(models.Model):
    is_occupied = models.BooleanField(default=False)
    seat = models.ForeignKey(Seat,  related_name="seats", on_delete=models.CASCADE)
    session = models.ForeignKey(Session, related_name="session_seats" ,on_delete=models.CASCADE)
    final_cost = models.FloatField(default=0)
    user = models.ForeignKey(User,related_name="tickets", on_delete=models.CASCADE)

class News(models.Model):
    text = models.TextField(max_length=2000)
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, related_name="news", on_delete=models.CASCADE)
    date = models.DateField()
    photo = models.ImageField(blank=True)

class Review(models.Model):
    text = models.TextField(max_length=2000)
    author = models.ForeignKey(User, related_name="reviews", on_delete=models.CASCADE)
    date = models.DateField()
    rate = models.IntegerField()
    movie = models.ForeignKey(Movie, related_name="reviews", on_delete=models.CASCADE)

class Post(models.Model):
    name = models.CharField(max_length=30)
    salary = models.FloatField()

class Employee(models.Model):
    user = models.OneToOneField(User,related_name="employee", on_delete=models.CASCADE)
    position = models.ForeignKey(Post, on_delete=models.CASCADE)
    photo = models.ImageField()

class FAQ(models.Model):
    question=models.CharField(max_length=200)
    answer = models.CharField(max_length=1000)
    date = models.DateField()

class Promo(models.Model):
    discount = models.FloatField()
    promo = models.CharField(max_length=20)
    
class Add(models.Model):
    photo = models.ImageField()
    url = models.CharField(max_length=1000)

class RotationSettings(models.Model):
    interval = models.IntegerField(default=1000000)