from django.contrib.auth.models import User
from django.db import models


class Hotel(models.Model):
    name = models.CharField(max_length=25)
    phone = models.CharField(max_length=12)
    info = models.TextField()


class Room(models.Model):
    capacity = models.IntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')


class RoomReservation(models.Model):
    guest = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
