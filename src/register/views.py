from django.http import request
from django.shortcuts import render
from .forms import RegisterForm
from django.shortcuts import redirect

# Create your views here.
def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")

    return render(request, "register/register.html", {"form" : form})
