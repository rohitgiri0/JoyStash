from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from CRUD.models import Snippet  

# Create your views here.


def loginform(request):
    if request.method == "POST":
        username = request.POST.get('uname')    
        password = request.POST.get('pass')
        next_url = request.POST.get('next')  # capture next if sent

        validate_user = authenticate(username=username, password=password)
        if validate_user is not None:
            login(request, validate_user)
            # Redirect to 'next' if provided, otherwise default home
            if next_url:
                return redirect(next_url)
            return redirect('homeapp:home')  # or your default home URL
        else:
            messages.error(request, "Wrong user details or user does not exist")
            return redirect('loginpage')
    
    # If GET, optionally pass next from query params to template
    next_url = request.GET.get('next', '')
    return render(request, 'users/loginpage.html', {'next': next_url})


def register(request):
    if request.method=="POST":
        username=request.POST.get('uname')
        email=request.POST.get('email')
        password=request.POST.get('pass')
        c_password=request.POST.get('c_pass')
        
        if password!=c_password:
            messages.error(request,"Please type the same password")
            return redirect('register')

        if len(password)<4:
            messages.error(request,"Password must be 4 characters long")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request,"Username already taken")
            return redirect('register')
        
        new_user=User.objects.create_user(username=username,email=email,password=password)
        new_user.save()
        messages.success(request,"User created successfully. login now")
        return redirect('loginpage')
    return render(request,'users/register.html',{})

def logout_view(request):
    logout(request)
    return render(request,'users/loginpage.html',{})
            
            
@login_required(login_url='loginpage') 
def dashboard(request):
    user = request.user
    total_snippets = Snippet.objects.filter(user=user).count()
    recent_snippets = Snippet.objects.filter(user=user).order_by('-created_at')[:10]  # last 10 snippets

    return render(request, 'users/profile.html', {
        'total_snippets': total_snippets,
        'recent_snippets': recent_snippets
    })

    


