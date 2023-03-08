from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .productAnalysis import product_analysis as PA
from .serviceAnalysis import service_analysis as SA

from productReceipt.models import Receipt_No as PRN
from serviceReceipt.models import Receipt_No as SRN
from django.utils import timezone

#Dashboard display
@login_required
def dashboard(request):


            
    
    today = timezone.now().date()
    product_today_receipt = PRN.objects.filter(
        user=request.user, created_at=today).order_by('-time_filter')
    service_today_receipt = SRN.objects.filter(
        user=request.user, created_at=today).order_by('-time_filter')

    srn = SRN.objects.filter(user = request.user)
    prn = PRN.objects.filter(user = request.user)
    context = {
        # 'weather_description': "http://openweathermap.org/img/w/" + weather_description + ".png",
        # 'temperature': round(current_temperature,4),
        'total': srn.count() + prn.count(),
        'total_receipt': PA()['total_receipt'] + SA()['total_receipt'],
        'today_receipt': PA()['today_receipt'] + SA()['today_receipt'],
        'this_week': PA()['this_week'] + SA()['this_week'],
        'this_month': PA()['this_month'] + SA()['this_month'],
        'product_today_receipt': product_today_receipt,
        'service_today_receipt': service_today_receipt,

       
    }
    
    return render(request, 'dashboard/dashboard.html', context)