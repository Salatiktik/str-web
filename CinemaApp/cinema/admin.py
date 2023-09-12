from django.contrib import admin
from .models import Movie,Genre,Hall,SeatType,Seat,Session,SessionSeat,Post,News,Review,Employee,FAQ
# Register your models here.
admin.site.register(Genre)
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("name","tickets_sum")

    def tickets_sum (self,obj):
        from django.db.models import Sum
        result = 0
        for i in SessionSeat.objects.filter(session__in = Session.objects.filter(movie = obj)):
            result+=i.seat.type.rate * i.session.price
        return round(result,2)


admin.site.register(Hall)
admin.site.register(SeatType)
admin.site.register(Seat)
@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("movie","startDate","startTime","tickets_sum",)
    
    def tickets_sum (self,obj):
        from django.db.models import Sum
        result = 0
        for i in SessionSeat.objects.filter(session = obj):
            result+=i.seat.type.rate * i.session.price
        return round(result,2)

admin.site.register(SessionSeat)
admin.site.register(News)
admin.site.register(Review)
admin.site.register(Post)
admin.site.register(Employee)
admin.site.register(FAQ)
