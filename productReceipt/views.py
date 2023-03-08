import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .forms import ItemForm, GenerateReceiptForm, UpdateItemForm
from productReceipt.models import Receipt_No, Item, get_receipt_no
from datetime import timedelta
from django.utils import timezone

from authentication.models import UserAccount, UserProfile
from django.db.models import Q

from .decorators import trial_satisfied

from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)
# Create your views here.


@login_required
def generate_receipt(request):

    
    userprofile = UserProfile.objects.get(user_id=request.user.id)
    if not userprofile.business_name:
        messages.error(request, "You need to update your profile first")
        return redirect("authentication:update-profile")

    if request.method == 'POST':
        form = GenerateReceiptForm(request.POST)
        
        if form.is_valid():
            form.save()
            
            receipt = Receipt_No.objects.get(receipt_no = get_receipt_no())
            
            return redirect('productReceipt:add_item', receipt.receipt_no)
        
    else:
        form = GenerateReceiptForm()
    context = {
        'form': form
    }
    return render(request, 'productReceipt/create-receipt.html', context)


@login_required
def all_invoice(request):

    userprofile = UserProfile.objects.get(user_id=request.user.id)
    if not userprofile.business_name:
        messages.error(request, "You need to update your profile first")
        return redirect("authenticationupdate-profile")

    all_invoice = Receipt_No.objects.filter(
        user=request.user).order_by('-time_filter')

    context = {
        'all_invoice': all_invoice
    }

    return render(request, 'productReceipt/allreceipt.html', context)


@login_required
def printed_today(request):

    userprofile = UserProfile.objects.get(user_id=request.user.id)
    if not userprofile.business_name:
        messages.error(request, "You need to update your profile first")
        return redirect("authentication:update-profile")

    today = timezone.now().date()
    today_receipt = Receipt_No.objects.filter(
        user=request.user, created_at=today).order_by('-time_filter')

    context = {
        'all_invoice': today_receipt
    }

    return render(request, 'productReceipt/allreceipt.html', context)


@login_required
def printed_this_week(request):

    userprofile = UserProfile.objects.get(user_id=request.user.id)
    if not userprofile.business_name:
        messages.error(request, "You need to update your profile first")
        return redirect("authentication:update-profile")

    date = datetime.datetime.today()

    week = date.strftime("%V")
    x = datetime.datetime.now()

    this_week = Receipt_No.objects.filter(
        user=request.user, created_at__week=week, created_at__year=x.year).order_by('-time_filter')

    context = {
        'all_invoice': this_week
    }

    return render(request, 'productReceipt/allreceipt.html', context)


@login_required
def printed_this_month(request):

    userprofile = UserProfile.objects.get(user_id=request.user.id)
    if not userprofile.business_name:
        messages.error(request, "You need to update your profile first")
        return redirect("authentication:update-profile")

    date = datetime.datetime.today()

    week = date.strftime("%V")
    x = datetime.datetime.now()
    print(x)
    this_month = Receipt_No.objects.filter(
        user=request.user, created_at__month=x.month, created_at__year=x.year).order_by('-time_filter')

    context = {
        'all_invoice': this_month
    }

    return render(request, 'productReceipt/allreceipt.html', context)


@login_required
def single_invoice(request, id, receipt_no):

    userprofile = UserProfile.objects.get(user_id=request.user.id)
    if not userprofile.business_name:
        messages.error(request, "You need to update your profile first")
        return redirect("authentication:update-profile")

    single_invoice = get_object_or_404(
        Receipt_No, user=request.user, id=id, receipt_no=receipt_no)
    items = Item.objects.filter(receipt_no_id=id)

    total = 0
    for item in items:
        total += item.get_sub_total()

    context = {
        'single_invoice': single_invoice,
        'items': items,
        'total': total,
        'item_count': items.count()

    }
    return render(request, 'productReceipt/single_invoice_view.html', context)



@login_required
def add_items(request, receipt_no):
    Receipt=Receipt_No.objects.get(receipt_no=receipt_no)
    userprofile = UserProfile.objects.get(user_id=request.user.id)
    if not userprofile.business_name:
        messages.error(request, "You need to update your profile first")
        return redirect("authentication:update-profile")

    if request.method == 'POST':
        form = ItemForm(request.POST)
        
        # receipt_no = request.GET['receipt_no']
        item_name = request.POST['item_name']
        item_price = request.POST['item_price']
        item_qty = request.POST['item_qty']
        item_desc = request.POST['item_desc']
        
        if form.is_valid():

            # form.save()
            item = Item(
                #receipt_no = receipt_no,
                item_name = item_name,
                item_price = item_price,
                item_qty = item_qty,
                item_desc = item_desc
            )
            Receipt = Receipt_No.objects.get(receipt_no=receipt_no)
            item.receipt_no = Receipt
            item.save()
            print("successful")
            return HttpResponseRedirect(request.path_info)
    else:
        form = ItemForm()
    context = {
        'form': form,
        'receipt_no': receipt_no,
        'receipt_no_id':Receipt.id
    }
    return render(request, 'productReceipt/item-form.html', context)


@login_required
def receipt_items(request, receipt_no):

    userprofile = UserProfile.objects.get(user_id=request.user.id)
    if not userprofile.business_name:
        messages.error(request, "You need to update your profile first")
        return redirect("authentication:update-profile")

    all_items = Item.objects.filter(receipt_no__receipt_no=receipt_no)
    receipt_no = Receipt_No.objects.get(receipt_no=receipt_no)
    print(receipt_no)
    context = {
        'all_items': all_items,
        'receipt_no': receipt_no
    }

    return render(request, 'productReceipt/receipt-items.html', context)


@login_required
def delete_single_item(request, id):

    item = get_object_or_404(Item, id=id)
    rn = item.receipt_no.receipt_no 
    item.delete()

    return redirect('productReceipt:all_items', rn)


@login_required
def approve(request, id):

    single_receipt = get_object_or_404(Receipt_No, id=id, user=request.user)

    if single_receipt.is_submitted:
        return redirect('dashboard:dashboard')

    single_receipt.is_submitted = True
    single_receipt.save()

    return redirect('productReceipt:single_invoice', id, single_receipt.receipt_no)


@login_required
def update_item(request, id):

    item = Item.objects.get(id=id)
    receipt_check = Receipt_No.objects.get(id=item.receipt_no.id)
    if receipt_check.is_submitted:
        return redirect('dashboard:dashboard')
    forms = UpdateItemForm(instance=item)

    if request.method == "POST":
        forms = UpdateItemForm(request.POST, instance=item)

        if forms.is_valid():
            forms.save()
            messages.success(request, "Item Updated Successfully")
            return redirect("productReceipt:all_items", item.receipt_no.receipt_no)

    context = {
        "forms": forms,
        "item": item
    }
    return render(request, "productReceipt/update_item.html", context)


def search(request):

    if 'keyword' in request.GET and request.GET['keyword'] is not None:
        keyword = request.GET['keyword']
        if keyword:
            all_invoice = Receipt_No.objects.order_by('-time_filter').filter(Q(receipt_no__icontains=keyword) | Q(
                receive_from__icontains=keyword) | Q(phone__icontains=keyword), user=request.user)
        else:
            return HttpResponseRedirect(request.path_info)
    else:
        return redirect('productReceipt:today')
    context = {
        'all_invoice': all_invoice
    }
    return render(request, 'productReceipt/allreceipt.html', context)

