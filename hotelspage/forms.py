from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Hotel, Room, User, RoomReservation


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['hotel']


class HotelForm(ModelForm):
    class Meta:
        model = Hotel
        fields = '__all__'



class RoomReservation(ModelForm):
    class Meta:
        model = RoomReservation
        fields = '__all__'
