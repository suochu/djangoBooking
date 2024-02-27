from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    custom_id = models.AutoField(primary_key=True)  # 新的自定義主鍵字段名稱
    # user 字段是一個指向 User 模型的一對一關係，Django 會自動處理 user_id
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    # 移除了手動創建的 user_id 字段
    username = models.CharField(max_length=100, unique=True)
    # Django 的 User 模型已包含安全處理密碼的機制，不需要在這裡重複
    profile_pic = models.ImageField(
        null=True, blank=True, default="profile1.png")
    phonenumber = models.CharField(max_length=15)
    membership = models.CharField(max_length=10, choices=[
                                  ('gold', 'Gold'), ('silver', 'Silver'), ('normal', 'Normal')])

    def __str__(self):
        return self.username


class Convenience(models.Model):
    convenienceId = models.AutoField(primary_key=True)
    # 移除null=True並添加default值
    name = models.CharField(max_length=100, default='Default Convenience Name')

    def __str__(self):
        return self.name


class Hotel(models.Model):
    hotel_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    CATEGORY = (
        ('five-star', 'five-star'),
        ('three-star', 'three-star'),
        ('one-star', 'one-star'),
    )
    city = models.CharField(max_length=30)
    image = models.ImageField(upload_to='hotelimages/', null=True, blank=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    description = models.CharField(max_length=30, blank=True)
    rating = models.DecimalField(max_digits=10, decimal_places=1)
    conveniences = models.ManyToManyField(Convenience)
    price = models.DecimalField(
        max_digits=8, decimal_places=2, default=0)  # 添加預設值

    def __str__(self):
        return f"{self.name} - {self.city}"


class Room(models.Model):
    ROOM_TYPES = (
        ('single', '單人房'),
        ('double', '標準雙人房'),
        ('suite', '豪華三人套房'),
    )
    room_id = models.AutoField(primary_key=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    roomtype = models.CharField(max_length=6, choices=ROOM_TYPES)
    price = models.IntegerField()
    capacity = models.IntegerField(
        default=1)  # 添加預設值
    conveniences = models.ManyToManyField(Convenience)
    image = models.ImageField(upload_to='roomImages/', null=True, blank=True)
    roomNumber = models.CharField(max_length=10, default=666)
    floor = models.IntegerField(default=5)
    totalRooms = models.IntegerField(default=5)

    def __str__(self):
        return f"{self.roomtype} - {self.hotel.name}"

    def is_available(self, check_in, check_out):
        # 查詢與此房間相關的所有預訂
        overlapping_bookings = Booking.objects.filter(
            room=self,
            check_in_date__lt=check_out,
            check_out_date__gt=check_in
        ).exists()
        # 如果存在重疊的預訂，則返回False
        return not overlapping_bookings


class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    total_price = models.IntegerField()

    def __str__(self):
        return f"Booking {self.booking_id}"


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=10, decimal_places=1)
    comment = models.TextField()

    def __str__(self):
        return f"Review {self.review_id} - {self.hotel.name}"


class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.IntegerField()
    date = models.DateField()
