from .models import Seat, SeatType, Hall

ec = SeatType.objects.get(name="econom")
st = SeatType.objects.get(name="standart")
vip = SeatType.objects.get(name="VIP")

bigHall=Hall.objects.get(id=1)
smallHall=Hall.objects.get(id=2)

for i in range(10):
    for j in range(15):
        Seat.objects.create(hall=bigHall,row=i+1,number=j+1,type=st)

for i in range(5):
    for j in range(10):
        Seat.objects.create(hall=smallHall,row=i+1,number=j+1,type=ec)