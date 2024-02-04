from . import views
from django.urls import path
from .views import hotel_list  # 確保從 views 模塊導入了 hotel_list 函數

urlpatterns = [
    path("", views.home, name="home"),
    path("join", views.join, name="join"),
    path('hotels', hotel_list, name='hotel_list'),  # 修改這裡的路徑配置


]
