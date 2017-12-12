from django.shortcuts import render
from basicapp.forms import UserForm,UserProfileInfoForm

# these imports are for the login and logout perspective

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout


# Create your views here.

def index(request):
    return render(request,'basicapp/index.html')

def register(request):

    registered  = False

    if request.method == 'POST':
        userform = UserForm(data=request.POST)
        profileform = UserProfileInfoForm(data = request.POST)

        if userform.is_valid() and profileform.is_valid():
            user = userform.save()
            user.set_password(user.password)
            user.save()

            profile = profileform.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()

            registered = True
        else:
            print(userform.errors,profileform.errors)
    else:
        userform = UserForm()
        profileform = UserProfileInfoForm()

    return render(request,'basicapp/register.html',{'userform':userform,'profileform':profileform,'registered':registered})

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user.is_active:
            login(request,user)

            return HttpResponseRedirect(reverse('index'))
        else:
            print("login Failed")

            return HttpResponse("invalid Credentials ")
    else:
        return render(request,'basicapp/login.html',{})
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def special(request):
    return HttpResponse("YOU ARE ACCESSING THIS IT MEANS YOU ARE LOGGED IN HURREY ")
