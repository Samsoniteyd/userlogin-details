from django.shortcuts import render,redirect
from . forms import CreateProfile, UpdateProfile
from django.contrib.auth.models import User

from django.contrib.auth import login,logout,authenticate

from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.



@login_required(login_url=('login'))
def index(request):
    return render(request, 'just/index.html' )


def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    form = CreateProfile()

    if request.method== 'POST':
        forms = CreateProfile(request.POST, request.FILES)
        if forms.is_valid():
            username = forms.cleaned_data.get('username')
            email = forms.cleaned_data.get('email')
            password = forms.cleaned_data.get('password1')
            password2 = forms.cleaned_data.get('password2')
            

            if User.objects.filter(username=username).exists():
                messages.warning(request, "username already exist")
        
                return redirect('register')
            if User.objects.filter(email=email).exists():
                messages.warning(request, "email already taken")
                
                return redirect('register')
            if password != password2:
                messages.warning(request, "password not match")
                   
                return redirect('register')

            user = User.objects.create_user(username,email,password) 
            forms= forms.save(commit=False)      
            forms.user = user
            forms.save()
 
            return redirect('login')
 
    context={
        'form': form
    }
    return render(request, 'just/register.html', context)

def loginuser(request):
    
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('passwd')

        user = authenticate(username= username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "login successfull.")
            return redirect('dashboard')
        else:
            messages.warning(request, "invalid username/password.")
            return redirect('login')

    return render(request, 'just/login.html')



def logoutuser(request):
    logout(request)
    messages.success(request, "logout successfull.")
    return redirect('login')

@login_required(login_url=('login'))
def dashboard(request):
    user = request.user.profile

    context= {
        'profile': user
    }
    return render(request, 'just/dashboard.html', context)





# update page
# update page


@login_required(login_url=('login'))

def update_profile(request):
    user = request.user.profile
    form = UpdateProfile(instance=user)
 
    if request.method == 'POST':
        forms = UpdateProfile(request.POST, request.FILES, instance=user)
        if forms.is_valid():
            forms.save()
            return redirect('dashboard')


    context= {
        'form': form
    }

    return render(request, 'just/update.html', context )
    