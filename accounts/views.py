from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from django.contrib import auth, messages
from .forms import UserLoginForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
# from usercontacts.models import Contact


# Create your views here.
def get_index(request):
    return render(request, "index.html")
    
def logout(request):
    auth.logout(request)
    messages.success(request, 'You have successfully logged out')
    return redirect(reverse('home'))
    
def login(request):
    if request.method=="POST":
        form=UserLoginForm(request.POST)
        
        if form.is_valid():
            user = auth.authenticate(username=form.cleaned_data['username'],
                                     password=form.cleaned_data['password'])

            if user is not None:
                auth.login(request, user)
                messages.error(request, "You have successfully logged in")
                
                if request.GET and request.GET['next'] !='':
                    next = request.GET['next']
                    return HttpResponseRedirect(next)
                else:
                    return redirect(profile)
                
            else:
                form.add_error(None, "Your user name is not recognised")
        
    else:
        form = UserLoginForm()
    
    return render(request, "login.html", {'form': form})      
    
def register(request):
    if request.method=="POST":
        form = UserRegistrationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            
            user = auth.authenticate(username=form.cleaned_data['username'],
                                     password=form.cleaned_data['password'])
                                     
            if user is not None:
                auth.login(request, user)
                return redirect(get_index)
            
            
    else:   
        form = UserRegistrationForm()
    
    
    return render(request, "register.html", {'form':form})
    
@login_required(login_url='/accounts/login')    
def profile(request):
    return render(request, "profile.html")