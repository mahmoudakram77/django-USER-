from django.shortcuts import render

from .forms import UserForm,UserProfileInfoForm
from django.urls import reverse
from django.http import HttpResponseRedirect , HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def index(request):
  return render(request, 'basicapp/index.html')
@login_required
def special(request):
  return HttpResponse('tou are logged in , nice!')


def register(request):

  registered = False
  
  if request.method == 'POST':
    user_form =UserForm(data=request.POST)
     
    profile_form = UserProfileInfoForm(data=request.POST)


    if user_form.is_valid() and profile_form.is_valid():
      user = user_form.save()
      user.set_password(user.password)
      user.save()

      profile =  profile_form.save(commit=False)
      profile.user = user
      if 'profile_pics' in request.FILES:
        profile.profile_pic = request.FILES['profile']
        profile.save()
    else:
      print(user_form.errors)
      print(profile_form.errors)
  else:
    user_form = UserForm()
    profile_form = UserProfileInfoForm()


  return render(request, 'basicapp/register.html',
                {'user_form':user_form,
                 'profile_form':profile_form,
                 'registered':registered, 
    
                 }
                )





# from django.urls import reverse
# from django.http import HttpResponseRedirect , HttpResponse
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import authenticate, login, logout


# def user_login(request):
#   if request.method == 'POST':
#     username = request.POST.get('username')
#     password = request.POST.get('password')
#     user = authenticate(username=username, password=password)

#     if user:
#       if user.is_active:
#         login(request, user)
#         return HttpResponseRedirect(reverse('index'))
#       else:
#         return HttpResponse("Account not active")
#     else:
#      print('someone trid to login and failed')
#      print('username: {} and password {}'.format(username,password))
#      return HttpResponse('INVALID LOGIN DETAIL SUPPLIED')
#   else:
#     return render(request, 'basicapp/login.html', {})
   
# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(username=username, password=password)

#         if user:
#             if user.is_active:
#                 login(request, user)
#                 # Redirect to a specific URL after login
#                 return HttpResponseRedirect(reverse('index'))
#             else:
#                 return HttpResponse("Your account is not active.")
#         else:
#             print(f"Invalid login attempt for username: {username}")
#             return HttpResponse("Invalid login details supplied.")
    
#     # If it's a GET request (show the login form)
#     else:
#         return render(request, 'basicapp/login.html')   

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        msg = ('you are count be access in this page')

        if user:
            if user.is_active:
                login(request, user)
                # Redirect to 'index' URL after successful login
                return HttpResponseRedirect(reverse('home'))
            else:
                message = "Account not active"
                return render(request, 'basicapp/login.html', {'message': message})
        else:
            message= 'invalid!'
            print(f"Invalid login attempt for username: {username}")
            return render(request, 'basicapp/login.html', {'message': message})
    
    # If it's a GET request (show the login form)
    else:
        return render(request, 'basicapp/login.html')
def user_logout(request):
  logout(request)
  return HttpResponseRedirect(reverse('home'))