from . import views
from django.urls import path
from .views import hotel_list  # 確保從 views 模塊導入了 hotel_list 函數
from .views import RoomListView, RoomDetailView


urlpatterns = [
    path("", views.home, name="home"),
    path('hotels', hotel_list, name='hotel_list'),  # 修改這裡的路徑配置
    path('hotels/<int:hotel_id>/rooms/',
         views.RoomsInAParticularHotel, name='RoomsInAParticularHotel'),
    path('addroom/', views.addroom, name='addroom'),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('user/', views.userPage, name="user-page"),
    path('customer/', views.customerSettings, name="customer"),
    path('rooms/', RoomListView.as_view(), name='room_list'),
    path('rooms/<int:pk>/', RoomDetailView.as_view(), name='room_detail'),
    path('check-availability/', views.check_room_availability,
         name='check_room_availability'),

    path('simple-checkout', views.simpleCheckout,
         name='simple_checkout'),
    path('payment-success/<int:room_id>/',
         views.PaymentSuccessful, name='payment-success'),
    path('payment-failed/<int:room_id>/',
         views.paymentFailed, name='payment-failed'),
    path('simple-checkout-membernull', views.simpleCheckoutMembernull,
         name='simple_checkout_membernull'),

    path('finalconfirmation/', views.finalconfirmation,
         name='finalconfirmation'),
    path('wait-for-cancellation/<int:booking_id>/',
         views.Waitforcancellation, name='waitforcancel'),

    path('confirmCancelBooking/<int:booking_id>/',
         views.confirmCancelBooking, name='confirmCancelBooking'),


]
