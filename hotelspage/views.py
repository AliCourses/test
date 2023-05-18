from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm

from .forms import HotelForm, RoomForm
from .models import Hotel, Room, RoomReservation
from . import forms

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages




def home(request):
    return render(request, "home.html")


@login_required(login_url='login')
def hotels(request):
    if not request.user.is_authenticated:
        return redirect('login')
    hotels = Hotel.objects.all()
    context = {'hotels': hotels}
    return render(request, "hotels.html", context)


def loginView(request):
    if request.user.is_authenticated:
        return redirect('hotels')

    if request.method == 'POST':
        u = request.POST["username"]
        p = request.POST["password"]
        user = authenticate(username=u, password=p)
        if user is not None:
            login(request, user)
            return redirect("hotels")
            # A backend authenticated the credential
        else:
            return redirect("login")
        # No backend authenticated the credentials

    else:
        form = AuthenticationForm()
        context = {'form': form}
        return render(request, 'login.html', context)


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('home')



def registerView(request):
    if request.user.is_authenticated:
        return redirect('hotels')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()

            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'register.html', context)




@login_required(login_url='login')
def addHotel(request):
    form = forms.HotelForm()
    if request.method == 'POST':
        Hotel.objects.create(
            name=request.POST["name"],
            phone=request.POST["phone"],
            info=request.POST["info"],
        )
        return redirect('hotels')
    context = {'form': form}
    return render(request, 'addHotel.html', context)


@login_required(login_url='login')
def addRoom(request, pk):
    if request.user.username != 'admin':
        return HttpResponse('Your are not allowed here!!')
    form = forms.RoomForm()
    if request.method == 'POST':
        Room.objects.create(
            capacity=int(request.POST["capacity"]),
            price=float(request.POST["price"]),
            hotel=Hotel.objects.get(id=pk)
        )
        return redirect('/rooms/' + str(pk))
    context = {'form': form}
    return render(request, 'addHotel.html', context)


@login_required(login_url='login')
def showRooms(request, pk):
    if request.user.is_authenticated:
        room_reservations = RoomReservation.objects.all()
        rooms = [reservation.room for reservation in room_reservations]
        unreserved_rooms = []
        allRooms = Room.objects.all()
        for room in allRooms:
            if (room not in rooms) and room.hotel.id == int(pk) :
                unreserved_rooms.append(room)
    return render(request, "rooms.html", {'rooms': unreserved_rooms, 'id': pk})


@login_required(login_url='login')
def MyRooms(request):
    if request.user.is_authenticated:
        room_reservations = RoomReservation.objects.all()
        myRooms = []

        for item in room_reservations:
            if item.guest == request.user:
                myRooms.append(item.room)
    return render(request, "myrooms.html", {'rooms': myRooms})


@login_required(login_url='login')
def deleteHotel(request, pk):
    hotel = Hotel.objects.get(id=pk)

    if request.user.username != 'admin':
        return HttpResponse('Your are not allowed here!!')

    hotel.delete()
    return redirect('hotels')


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user.username != 'admin':
        return HttpResponse('Your are not allowed here!!')

    room.delete()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def reserveRoom(request, pk):
    room = Room.objects.get(pk=pk)

    if RoomReservation.objects.filter(guest=request.user, room=room).exists():
        messages.warning(request, f"You have already reserved room {room.id}")
        return redirect('room_detail', room_id=pk)

    RoomReservation.objects.create(guest=request.user, room=room)
    messages.success(request, f"Room {room.id} has been reserved successfully.")
    return redirect(request.META.get('HTTP_REFERER'), room_id=pk)


@login_required(login_url='login')
def unreserveRoom(request, pk):
    room = Room.objects.get(pk=pk)
    reservation = RoomReservation.objects.filter(guest=request.user, room=room)

    if not reservation.exists():
        messages.warning(request, f"You have not reserved room {room.id}")
        return redirect('room_detail', room_id=pk)

    reservation.delete()
    messages.success(request, f"Reservation for room {room.id} has been cancelled.")
    return redirect(request.META.get('HTTP_REFERER'), room_id=pk)

@login_required(login_url='login')
def updateHotel(request, pk):
    post = Hotel.objects.get(pk=pk)
    if request.method == 'POST':
        form = HotelForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect('hotels')
    else:
        form = HotelForm(instance=post)
    return render(request, 'updateHotel.html', {'form': form})


@login_required(login_url='login')
def updateRoom(request, pk):
    post = Room.objects.get(pk=pk)
    hotelId = post.hotel.id;
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect("/rooms/"+str(hotelId))
    else:
        form = RoomForm(instance=post)
    return render(request, 'updateRoom.html', {'form': form})
