from django.db import models

# Create your models here.
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
import datetime

from authentication.models import UserAccount

from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)

class Receipt_No(models.Model):
    CURRENCY_CHOICES = (
            ('N', 'N'),
            ('$', '$'),
            ('EURO', 'EURO'),

        )
    user = models.ForeignKey(UserAccount, related_name="serviceuser", default=UserAccount, on_delete=models.CASCADE, null=True)
    receipt_no = models.CharField(max_length=500, unique=True, null=True, blank=True)
    receive_from = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=11)
    currency_format = models.CharField(max_length=10, choices=CURRENCY_CHOICES)
    is_submitted = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    time_filter = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.receipt_no} - {self.receive_from}"
    
    def get_receipt_no(self):
        return f"{self.receipt_no}"
    class meta:
        ordering = ['time_filter']

@receiver(post_save, sender=Receipt_No)
def create_receipt(sender, instance, created, **kwargs):

    global newreceiptno
    user = UserAccount.objects.get(id = get_current_authenticated_user().id)
    r = Receipt_No.objects.get(id = instance.id)
    
    if created:
        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr,mt,dt)
        current_date = d.strftime("%Y%m%d")
        if instance.id <= 9:
            pad_no = "00"
        elif instance.id >=10 and instance.id < 100:
            pad_no = "0"
        else: 
            pad_no = ""
        receipt_no = current_date +"-"+str(get_current_authenticated_user().id)+"-"+pad_no+str(user.number_count)
        r.receipt_no = receipt_no
        newreceiptno = receipt_no
        r.user = get_current_authenticated_user()       
        r.save()
        user.number_count +=1
        user.save()
    else:
        pass

class Item(models.Model):
    receipt_no = models.ForeignKey(Receipt_No, default=Receipt_No, on_delete=models.CASCADE, related_name="servicereceiptno", blank=True, null= True)
    item_name = models.CharField(max_length=50)
    item_price = models.IntegerField()
    item_desc = models.CharField(max_length=250)
    def __str__(self):
        return f"{self.item_name} - {self.receipt_no}"

    def get_sub_total(self):
        return self.item_price

    
def get_receipt_no():
    return newreceiptno

