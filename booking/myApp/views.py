from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect, get_object_or_404
from .models import Hotel, Room, Convenience, Customer, Booking
from .forms import CreateUserForm, CustomerForm, Roomform
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group
from .filters import RoomFilter
from django.views.decorators.http import require_http_methods
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.urls import reverse
from django.db import IntegrityError

from django.contrib.auth.models import User
from django.http import HttpResponse


class RoomListView(ListView):
    model = Room
    template_name = 'myApp/roomList.html'
    context_object_name = 'rooms'

    def get_queryset(self):
        # 使用 RoomFilter 來過濾數據
        self.filter = RoomFilter(
            self.request.GET, queryset=super().get_queryset())
        return self.filter.qs

    def get_context_data(self, **kwargs):
        # 將 filter 添加到上下文中，這樣它就可以在模板中被訪問和渲染
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter
        return context


class RoomDetailView(DetailView):

    model = Room
    template_name = 'myApp/roomDetail.html'
    context_object_name = 'room'

    def get(self, request, *args, **kwargs):
        # 通過URL捕獲的pk參數即為room_id
        room_id = self.kwargs.get('pk')
        # 將room_id存儲到session中
        request.session['room_id'] = room_id
        # 繼續執行父類的get方法
        return super(RoomDetailView, self).get(request, *args, **kwargs)


def RoomsInAParticularHotel(request, hotel_id):

    hotel = get_object_or_404(Hotel, pk=hotel_id)  # 獲取特定酒店

    available_rooms = Room.objects.filter(hotel=hotel)  # 返回特定酒店的所有房間
    # 獲取該酒店中所有不重複的房型

    room_types = list(available_rooms.order_by(
        'roomtype').values_list('roomtype', flat=True).distinct())

    return render(request, 'myApp/availableRooms.html', {
        'hotel': hotel,
        'availableRooms': available_rooms,
        'room_types': room_types  # 將房型列表傳遞給模板
    })


@unauthenticated_user
def registerPage(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_name = request.POST['username']
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            # 註冊會員同時創建會員資料檔案Customer
            Customer.objects.create(
                user=user,
                username=user_name,
                profile_pic='profile1.png',  # 使用默認圖片
                phonenumber='',  # 假設您的模型允許空字符串
                membership='normal',  # 設置默認會員等級為'normal'
            )
            messages.success(
                request, f'Account was created for {user_name}')
            return redirect('login')
        else:
            for msg in form.errors:
                messages.error(request, form.errors[msg])
    else:
        form = CreateUserForm()

    context = {'form': form}
    return render(request, 'myApp/register.html', context)


@unauthenticated_user
def loginPage(request):
    # 如果收到一個 POST 請求，則進行處理
    if request.method == 'POST':
        # 從 POST 數據中獲取用戶名和密碼
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 使用 Django 的 authenticate 函數嘗試認證用戶
        user = authenticate(request, username=username, password=password)
        # 如果authenticate方法返回了用户对象，表示认证成功
        if user is not None:
            # 使用login方法来登录用户，这会在后端创建用户会话
            login(request, user)
            # 重定向到主页，'home'是主页的URL名称
            return redirect('hotel_list')
        else:
            # 如果认证失败，向用户显示错误信息
            messages.info(request, 'Username OR password is incorrect')

    return render(request, "myApp/login.html", {})


def logoutUser(request):
    logout(request)
    return redirect('login')


def hotels(request):
    all_Hotels = Hotel.objects.all
    return render(request, "myApp/hotels.html", {'all': all_Hotels})


@login_required(login_url='login')
@admin_only
def home(request):
    all_Hotels = Hotel.objects.all
    return render(request, "myApp/home.html", {'all': all_Hotels})


def hotel_list(request):
    # 獲取查詢參數中所有的 "facilities" 值
    facility_queries = request.GET.getlist('facilities')
    print(facility_queries)  # ['free_wifi', 'nonsmoking']

    if facility_queries:
        hotels = Hotel.objects.all()
        for Facility_name in facility_queries:
            hotels = Hotel.objects.filter(conveniences__name=Facility_name)
        print(hotels.query)
    else:
        # 如果沒有指定設施查詢參數，則返回所有酒店
        hotels = Hotel.objects.all()

    return render(request, "myApp/hotels.html", {'all': hotels})


@login_required(login_url='login')
@admin_only
def addroom(request):
    # 在处理请求的任何部分之前定义变量
    hotels = Hotel.objects.all()  # 获取所有酒店列表
    roomtypes = Room.ROOM_TYPES  # 直接从Room模型访问ROOM_TYPES
    conveniences = Convenience.objects.all()

    if request.method == "POST":
        form = Roomform(request.POST or None)
        if form.is_valid():
            form.save()
            # 可选：在成功保存表单后，可以重定向到一个新的URL，或者再次渲染表单以显示成功消息
        else:
            hotel = request.POST.get('hotel')
            roomtype = request.POST.get('roomtype')
            price = request.POST.get('price')
            availability = request.POST.get('availability')
            capacity = request.POST.get('capacity')
            conveniences = request.POST.get('Conveniences')
            print(form.errors)
            messages.success(request, ('add room error! Try agin'))
            # return redirect('join')不用redierct的原因 借用原本的request保存資料
            return render(request, "myApp/addroom.html", {



            })
        messages.success(request, ('add room Successful'))
        return redirect('hotel_list')
    # 注意：POST处理逻辑中不再有对hotels, room_types, Facilitys变量的定义，
    # 因为它们已经在函数开始处被定义

    # 使用相同的变量渲染模板
    return render(request, "myApp/addroom.html", {'hotels': hotels, 'roomtypes':  roomtypes, 'conveniences': conveniences})


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    bookings = request.user.customer.booking_set.all()
    print('BOOKINGS:', bookings)
    context = {'bookings': bookings}
    return render(request, "myApp/user.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def confirmCancelBooking(request, booking_id):
    booking = get_object_or_404(
        Booking, booking_id=booking_id, user=request.user.customer)
    Booking.objects.filter(pk=booking_id).delete()

    context = {'booking': booking}
    return render(request, "myApp/bookingCancel.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def Waitforcancellation(request, booking_id):
    # 獲取booking_id可以判定就是要取消?
    booking = get_object_or_404(
        Booking, booking_id=booking_id, user=request.user.customer)

    context = {'booking': booking}
    return render(request, "myApp/Waitforcancellation.html", context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def customerSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, "myApp/customer_settings.html", context)


@require_http_methods(["GET", "POST"])
def check_room_availability(request):
    if request.method == 'POST':
        hotel_id = request.POST.get('hotelId')
        hotel = get_object_or_404(Hotel, pk=hotel_id)
        room_type = request.POST.get('roomtype')
        check_in = request.POST.get('checkin')
        check_out = request.POST.get('checkout')
        print(check_in)
        print(check_out)

        request.session['check_in_date'] = check_in
        request.session['check_out_date'] = check_out

        room_types = Room.objects.filter(hotel=hotel).values_list(
            'roomtype', flat=True).distinct()

        available_rooms = Room.objects.filter(
            Q(hotel=hotel_id) &
            Q(roomtype=room_type) &
            ~Q(
                booking__check_in_date__lt=check_out,
                booking__check_out_date__gt=check_in
            )
        ).distinct()
        print(available_rooms)
    else:
        available_rooms = Room.objects.none()  # 如果不是POST請求，不顯示任何房間

    return render(request, 'myApp/availableRooms.html', {'hotel': hotel, 'availableRooms': available_rooms, 'room_types':  room_types, 'check_in': check_in, 'check_out': check_out})


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def simpleCheckout(request):
    room_id = request.GET.get('room_id')
    request.session['room_id'] = room_id
    if room_id:
        # 執行下訂相關的操作
        room = Room.objects.get(room_id=room_id)
        host = request.get_host()
        paypal_checkout = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': room.price,
            'item_name': f"{room.hotel.name} - {room.roomtype}",
            'invoice': uuid.uuid4(),
            'notify_url': f"http://{host}{reverse('paypal-ipn')}",
            'return_url': f"http://{host}{reverse('user-page')}",
            'cancel_url': f"http://{host}{reverse('payment-failed', kwargs={'room_id': room.room_id})}",

        }

        paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

        context = {
            'room':  room,
            'paypal': paypal_payment
        }

        return render(request, 'myApp/simple_checkout.html', context)

    else:
        # 如果沒有提供room_id，處理錯誤或重定向
        return HttpResponse("錯誤：未提供房間ID")


def simpleCheckoutMembernull(request):
    # 註冊user
    # 增添會員檔案customer
    room_id = request.session.get('room_id')
    check_in_date = request.session.get('check_in_date')
    check_out_date = request.session.get('check_out_date')
    if room_id:
        # 執行下訂相關的操作
        room = Room.objects.get(room_id=room_id)
        total_price = room.price
        context = {
            'room':  room,
            'check_in_date': check_in_date,
            'check_out_date': check_out_date,
            'total_price': total_price,
        }

        return render(request, 'myApp/simple_checkout_membernull.html', context)

    else:
        # 如果沒有提供room_id，處理錯誤或重定向 這種狀況是不能出現的
        return HttpResponse("錯誤：未提供房間ID")


def finalconfirmation(request):
    if request.method == 'POST':
        room_id = request.session.get('room_id')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        # 检查用户名是否已存在
        if User.objects.filter(username=username).exists():
            # 如果用户名已存在，返回错误信息
            messages.error(request, 'Username already exists.')  # 添加一條錯誤消息
            return redirect('simple_checkout_membernull')

        # 创建user用户
        try:
            user = User.objects.create_user(
                username=username, password=password, email=email)
        except IntegrityError:
            messages.error(request, 'Username already exists.')  # 添加一條錯誤消息
            return redirect('An error occurred creating the user.')
            # 如果仍然遇到IntegrityError，进行错误处理

        group = Group.objects.get(name='customer')
        user.groups.add(group)
        # 創建Customer用戶個人資料檔案
        # 使用login方法来登录用户，这会在后端创建用户会话
        login(request, user)
        Customer.objects.create(
            user=user,
            username=username,
            profile_pic='profile1.png',  # 使用默认图片
            phonenumber='',  # 假设您的模型允许空字符串
            membership='normal',  # 设置默认会员等级为'normal'
        )
        if room_id:
            # 執行下訂相關的操作
            room = Room.objects.get(room_id=room_id)
            host = request.get_host()
            paypal_checkout = {
                'business': settings.PAYPAL_RECEIVER_EMAIL,
                'amount': room.price,
                'item_name': f"{room.hotel.name} - {room.roomtype}",
                'invoice': uuid.uuid4(),
                'notify_url': f"http://{host}{reverse('paypal-ipn')}",
                'return_url': f"http://{host}{reverse('payment-success', kwargs={'room_id': room.room_id})}",
                'cancel_url': f"http://{host}{reverse('payment-failed', kwargs={'room_id': room.room_id})}",
            }

            paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

            context = {
                'room':  room,
                'paypal': paypal_payment
            }

            return render(request, 'myApp/simple_checkout.html', context)

    else:
        return render(request, 'myApp/simple_checkout_membernull.html', {})


def PaymentSuccessful(request, room_id):

    room = get_object_or_404(Room, room_id=room_id)
    user = request.user.customer  # 假设用户已登录并可通过request.user获取
    check_in_date = request.session.get('check_in_date')
    check_out_date = request.session.get('check_out_date')
    total_price = room.price

    if not all([check_in_date, check_out_date, total_price]):
        # 如果缺少信息，重定向到一个错误页面或显示错误消息
        messages.error(request, "缺少预订所需的信息。")
        return redirect('some_error_page')

    # 创建新的预订记录
    booking = Booking.objects.create(
        user=user,
        hotel=room.hotel,
        room=room,
        check_in_date=check_in_date,
        check_out_date=check_out_date,
        total_price=total_price
    )

    for key in ['check_in_date', 'check_out_date', 'total_price']:
        if key in request.session:
            del request.session[key]

    return render(request, 'myApp/paymentsuccess.html', {'room': room, 'booking': booking})


def paymentFailed(request, room_id):

    room = Room.objects.get(room_id=room_id)

    return render(request, 'myApp/paymentfailed.html',  {'room': room})
