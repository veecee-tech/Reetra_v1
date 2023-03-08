from django.contrib import admin
from home.models import ContactUs
# Register your models here.


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
