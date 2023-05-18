from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerView, name='register'),
    path("hotels/", views.hotels, name="hotels"),
    path("", views.home, name="home"),
    path("login/", views.loginView, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("signup/", views.registerView, name="signup"),
    path("addHotel/", views.addHotel, name="addhotel"),
    path("addRoom/<int:pk>", views.addRoom, name="addroom"),
    path("rooms/<int:pk>", views.showRooms, name="showrooms"),
    path("myRooms/", views.MyRooms, name="myRooms"),
    path("delete/<int:pk>", views.deleteHotel, name="deletehotel"),
    path("deleteRoom/<int:pk>", views.deleteRoom, name="deleteRoom"),
    path("reserveRoom/<int:pk>", views.reserveRoom, name="reserveRoom"),
    path("unreserveRoom/<int:pk>", views.unreserveRoom, name="unreserveRoom"),
    path("updateHotel/<int:pk>",views.updateHotel,name="updateHotel"),
path("updateRoom/<int:pk>",views.updateRoom,name="updateRoom"),

]
