from django.shortcuts import redirect, render, HttpResponseRedirect
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from authentication.models import UserAccount
from django.contrib.auth import update_session_auth_hash
from .forms import UserProfileForm, RegistrationForm
import requests
# Create your views here.


def register(request):

    res = requests.get('https://restcountries.com/v2/all')

    country_code = res.json()
   
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        phone_code = request.POST.get('phone_code')
        if form.is_valid():
            
            striped_phone = None
            actual_phone = form.cleaned_data['phone']
            print(actual_phone[0])
            if actual_phone[0] == '0':
                
                striped_phone = actual_phone[1:]
            else:
                striped_phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            phone = phone_code+striped_phone
            password = form.cleaned_data['password']
            username = form.cleaned_data['username']
            check_policy = request.POST.get('checkPolicy')

            if check_policy:
                user = UserAccount.objects.create_user(
                    username=username.strip(),
                    phone=phone,
                    email = email,
                    password = password
                    )
                user.is_active = True
                user.save()

                messages.success(request, "Registration Successful")
                return redirect('authentication:login')
            else:
                messages.error(request, "You need to accept our Terms and Conditions")
                return HttpResponseRedirect(request.path_info)
    else:
        form = RegistrationForm()
    context = {
        'form': form,
        'country_code': ['+'+x['callingCodes'][0] for x in country_code],
       
    }
    return render(request, 'authentication/signup.html', context)

def login(request):

    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username = username, password = password)

        if user is not None:
            auth.login(request,user)
            return redirect('dashboard:dashboard')
        else:
            messages.error(request, 'invalid username or password')
            return redirect('authentication:login')

    return render(request, 'authentication/signin.html')

@login_required
def logout(request):
    auth.logout(request)
    return redirect('home')

@login_required
def change_password(request):

    user = UserAccount.objects.get(username__exact = request.user.username)         
    if request.method == 'POST':

        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        success = user.check_password(old_password)

        if success:
            if new_password == confirm_password:
                user.set_password(new_password)
                update_session_auth_hash(request, user)
                user.save()
                messages.error(request, "password changed successfully")
                return redirect('change-password')
            else:
                messages.error(request, "password mismatch")
                return redirect('authentication:change-password')

        else:
            messages.error(request, "invalid old password")
            return redirect('authentication:change-password')
    return render(request, 'authentication/changepassword.html')



@login_required 
def user_profile_view(request):
    forms = UserProfileForm(instance=request.user.userprofile)
    
    if request.method == "POST":
        forms =UserProfileForm(request.POST, request.FILES or None, instance=request.user.userprofile)

        if forms.is_valid():
            forms.save()
            messages.success(request, "Profile Updated successfully")
            return redirect("authentication:update-profile")

    context = {
        "forms": forms,
    }
    return render(request, "authentication/profile.html", context)
