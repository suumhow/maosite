from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_funct):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('mydashboard')
        else:
            return view_funct(request, *args, **kwargs)
    return wrapper_func

def authenticated_user(view_funct):
    def wrapper_func(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        else:
            return view_funct(request, *args, **kwargs)
    return wrapper_func