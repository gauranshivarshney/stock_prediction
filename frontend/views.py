from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Prediction
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from ml.utils import predict_next_price

def base(request):
    return render(request, 'home.html')

def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        from django.contrib.auth.models import User
        User.objects.create_user(username=username, password=password)
        return redirect("/login")
    return render(request, "register.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("/dashboard")
    return render(request, "login.html")

@login_required
def dashboard_view(request):
    return render(request, "dashboard.html")