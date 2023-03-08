from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect
from authentication.models import UserAccount
from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)

def trial_satisfied(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):

        users = UserAccount.objects.get(id = get_current_authenticated_user().id)
        trial_version_exceeded = users.get_is_trial_version_exceeded()
        if trial_version_exceeded:
            messages.error(request, "Trial Limit Exceeded, Contact Startechone Nigeria Limited for Upgrade" )
            # auth.logout(request)
            return redirect('dashboard')
        else:
            return function(request, *args, **kwargs)
    return wrap