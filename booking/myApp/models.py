from django.db import models

# HotelID：唯一識別碼 # Name：酒店名稱 # city：地區
# Description：描述 # Rating：評分
# 内容需包含hotel_pic飯店的圖片、起價


class Facility(models.Model):
    name = models.CharField(max_length=100, null=True)

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
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    description = models.CharField(max_length=30, blank=True)
    rating = models.DecimalField(max_digits=10, decimal_places=1)
    facilities = models.ManyToManyField(Facility)
    price = models.DecimalField(
        max_digits=8, decimal_places=2, default=0)  # 添加預設值

    def __str__(self):
        return f"{self.name} - {self.city}"


class Room(models.Model):
    room_id = models.AutoField(primary_key=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_type = models.CharField(max_length=30)
    price = models.IntegerField()
    availability = models.BooleanField()

    def __str__(self):
        return f"{self.room_type} - {self.hotel.name}"


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    # 實際情況應使用Django的內建用戶模型，它會安全地處理密碼。
    password = models.CharField(max_length=128)
    phonenumber = models.CharField(max_length=15)
    membership = models.CharField(max_length=10, choices=[
                                  ('gold', 'Gold'), ('silver', 'Silver')])

    def __str__(self):
        return self.username


class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=10, decimal_places=1)
    comment = models.TextField()

    def __str__(self):
        return f"Review {self.review_id} - {self.hotel.name}"


class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    date = models.DateField()
