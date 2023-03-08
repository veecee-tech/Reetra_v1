from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
# from django.core.mail import send_mail
from home.models import ContactUs
from django.contrib import messages


class Home(TemplateView):

    template_name = ('home/index.html')

class Privacy(TemplateView):
    
    template_name = ('home/privacypolicy.html')


def contactUsView(request):

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        email_message = request.POST.get('message')
        subject = request.POST.get('subject')
        send = ContactUs(name=name, email=email, message = email_message)

        send.save()
        # email_subject = f'New contact {email}: {subject}'

        # send_mail(email_subject, email_message, 'jethrovictor68@gmail.com', ['jethrovictor68@gmail.com',])
        messages.success(request, 'Response Received and processing')
        return redirect('home')