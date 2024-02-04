from django.shortcuts import render, redirect
from .models import Hotel
from .forms import Userform, Facilityform
from django.contrib import messages
from django.db.models import Q


def hotels(request):
    all_Hotels = Hotel.objects.all
    return render(request, "myApp/hotels.html", {'all': all_Hotels})


def home(request):
    all_Hotels = Hotel.objects.all
    return render(request, "myApp/home.html", {'all': all_Hotels})


def join(request):
    if request.method == "POST":
        form = Userform(request.POST or None)
        if form.is_valid():
            form.save()
        else:
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            phonenumber = request.POST['phonenumber']
            messages.success(request, ('Registration error! Try agin'))
            # return redirect('join')不用redierct的原因 借用原本的request保存資料
            return render(request, "myApp/join.html", {
                'username': username,
                'email': email,
                'password': password,
                'phonenumber': phonenumber,

            })
        messages.success(request, ('User Registration Successful'))
        return redirect('home')
    else:
        return render(request, "myApp/join.html", {})


def hotel_list(request):
    # 獲取查詢參數中所有的 "facilities" 值
    facility_queries = request.GET.getlist('facilities')
    print(facility_queries)  # ['free_wifi', 'nonsmoking']

    if facility_queries:
        hotels = Hotel.objects.all()
        for Facility_name in facility_queries:
            hotels = Hotel.objects.filter(facilities__name=Facility_name)
        print(hotels.query)
    else:
        # 如果沒有指定設施查詢參數，則返回所有酒店
        hotels = Hotel.objects.all()

    return render(request, "myApp/hotels.html", {'all': hotels})
