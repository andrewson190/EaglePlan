from django.shortcuts import render
from .forms import RegisterForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


# Create your views here.

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
           #new_user = form.save()

            #new_user = authenticate(username=form.cleaned_data['username'],
                           #         password=form.cleaned_data['password1'],
                            #        )
           # login(request, new_user)
            admin_check = form.cleaned_data.get('isAdmin')
            if admin_check:
                return redirect('admin_register/')
            else:
                return redirect('student_register/')

    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})

