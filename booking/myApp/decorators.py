from django.http import HttpResponse
from django.shortcuts import redirect

# 這是一個自定義裝飾器，旨在限制已經認證的用戶訪問特定視圖


def unauthenticated_user(view_func):
    # 裝飾器內部的包裹函數
    def wrapper_func(request, *args, **kwargs):
        # 如果當前用戶已經認證，重定向到首頁
        if request.user.is_authenticated:
            return redirect('home')
        else:
            # 否則，繼續執行原本的視圖函數
            return view_func(request, *args, **kwargs)
    return wrapper_func

#


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('you are not authorized to view this page')
        return wrapper_func
    return decorator


def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'customer':
            return redirect('user-page')
        if group == 'admin':
            return view_func(request, *args, **kwargs)
    return wrapper_function
