from serviceReceipt.models import Receipt_No as SRN, Item as SRI
import datetime
from django.utils import timezone
from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)


#Product Receipt Analysis

def service_analysis():
    
    date = datetime.datetime.today()
    
    week = date.strftime("%V")
    
    x = datetime.datetime.now()

    this_week = SRN.objects.filter(
        user_id=get_current_authenticated_user().id, created_at__week=week, created_at__year=x.year)
    
    today = timezone.now().date()
    
    this_month = SRN.objects.filter(
        user_id=get_current_authenticated_user().id, created_at__month=x.month, created_at__year=x.year)
    total_receipt = SRN.objects.filter(user_id=get_current_authenticated_user().id)

    today_receipt = SRN.objects.filter(
        user_id=get_current_authenticated_user().id, created_at=today)

    
# #week analysis
#     sun_data = SRN.objects.filter(
#         user_id=get_current_authenticated_user().id, created_at__month=x.month, created_at__year=x.year, created_at__week=week, created_at__week_day=1)
#     mon_data = SRN.objects.filter(
#         user_id=get_current_authenticated_user().id, created_at__month=x.month, created_at__year=x.year,created_at__week=week, created_at__week_day=2)
#     tue_data = SRN.objects.filter(
#         user_id=get_current_authenticated_user().id, created_at__month=x.month, created_at__year=x.year,created_at__week=week, created_at__week_day=3)
#     wed_data = SRN.objects.filter(
#         user_id=get_current_authenticated_user().id, created_at__month=x.month, created_at__year=x.year,created_at__week=week, created_at__week_day=4)
#     thur_data = SRN.objects.filter(
#         user_id=get_current_authenticated_user().id, created_at__month=x.month, created_at__year=x.year,created_at__week=week, created_at__week_day=5)
#     fri_data = SRN.objects.filter(
#         user_id=get_current_authenticated_user().id, created_at__month=x.month, created_at__year=x.year,created_at__week=week, created_at__week_day=6)
#     sat_data = SRN.objects.filter(
#         user_id=get_current_authenticated_user().id, created_at__month=x.month, created_at__year=x.year,created_at__week=week, created_at__week_day=7)

#     #year analysis
#     jan_data = SRN.objects.filter(
#         user_id=get_current_authenticated_user().id, created_at__month = 1, created_at__year=x.year)
#     jan_items = SRI.objects.filter(receipt_no__user_id=get_current_authenticated_user().id, receipt_no__created_at__month = 1, receipt_no__created_at__year=x.year)
#     total_sales_jan = 0
#     for jan_item in jan_items:
#         total_sales_jan += jan_item.get_sub_total()

#     feb_data = SRN.objects.filter(
#         user_id=get_current_authenticated_user().id, created_at__month = 2, created_at__year=x.year)
#     feb_items = SRI.objects.filter(receipt_no__user_id=get_current_authenticated_user().id, receipt_no__created_at__month = 2, receipt_no__created_at__year=x.year)
#     total_sales_feb = 0
#     for feb_item in feb_items:
#         total_sales_feb += feb_item.get_sub_total()

#     mar_data = SRN.objects.filter(
#         user_id=get_current_authenticated_user().id, created_at__month = 3, created_at__year=x.year)
#     mar_items = SRI.objects.filter(receipt_no__user_id=get_current_authenticated_user().id, receipt_no__created_at__month = 3, receipt_no__created_at__year=x.year)
#     total_sales_mar = 0
#     for mar_item in mar_items:
#         total_sales_mar += mar_item.get_sub_total()

#     apr_data = SRN.objects.filter(
#         user_id=get_current_authenticated_user().id, created_at__month = 4, created_at__year=x.year)
#     apr_items = SRI.objects.filter(receipt_no__user_id=get_current_authenticated_user().id, receipt_no__created_at__month = 4, receipt_no__created_at__year=x.year)
#     total_sales_apr = 0
#     for apr_item in apr_items:
#         total_sales_apr += apr_item.get_sub_total()

    

#     may_data = SRN.objects.filter(
#         user_id=get_current_authenticated_user().id, created_at__month = 5, created_at__year=x.year)
#     may_items = SRI.objects.filter(receipt_no__user_id=get_current_authenticated_user().id, receipt_no__created_at__month = 5, receipt_no__created_at__year=x.year)
#     total_sales_may = 0
#     for may_item in may_items:
#         total_sales_may += may_item.get_sub_total()
    
#     jun_data = SRN.objects.filter(
#         user_id=get_current_authenticated_user().id, created_at__month = 6, created_at__year=x.year)
#     jun_items = SRI.objects.filter(receipt_no__user_id=get_current_authenticated_user().id, receipt_no__created_at__month = 6, receipt_no__created_at__year=x.year)
#     total_sales_jun = 0
#     for jun_item in jun_items:
#         total_sales_jun += jun_item.get_sub_total()

#     jul_data = SRN.objects.filter(
#         user_id=get_current_authenticated_user().id, created_at__month = 7, created_at__year=x.year)
#     jul_items = SRI.objects.filter(receipt_no__user_id=get_current_authenticated_user().id, receipt_no__created_at__month = 7, receipt_no__created_at__year=x.year)
#     total_sales_jul = 0
#     for jul_item in jul_items:
#         total_sales_jul += jul_item.get_sub_total()

#     #august
#     aug_data = SRN.objects.filter(
#         user_id=get_current_authenticated_user().id, created_at__month = 8, created_at__year=x.year)
#     aug_items = SRI.objects.filter(receipt_no__user_id=get_current_authenticated_user().id, receipt_no__created_at__month = 8, receipt_no__created_at__year=x.year)
#     total_sales_aug = 0
#     for aug_item in aug_items:
#         total_sales_aug += aug_item.get_sub_total()
    
#     #september
#     sep_data = SRN.objects.filter(
#         user_id=get_current_authenticated_user().id, created_at__month = 9, created_at__year=x.year)
#     sep_items = SRI.objects.filter(receipt_no__user_id=get_current_authenticated_user().id, receipt_no__created_at__month = 9, receipt_no__created_at__year=x.year)
#     total_sales_sep = 0
#     for sep_item in sep_items:
#         total_sales_sep += sep_item.get_sub_total()

#     #october
#     oct_data = SRN.objects.filter(
#         user_id=get_current_authenticated_user().id, created_at__month = 10, created_at__year=x.year)
#     oct_items = SRI.objects.filter(receipt_no__user_id=get_current_authenticated_user().id, receipt_no__created_at__month = 10, receipt_no__created_at__year=x.year)
#     total_sales_oct = 0
#     for oct_item in oct_items:
#         total_sales_oct += oct_item.get_sub_total()
    
#     #november
#     nov_data = SRN.objects.filter(
#         user_id=get_current_authenticated_user().id, created_at__month = 11, created_at__year=x.year)
#     nov_items = SRI.objects.filter(receipt_no__user_id=get_current_authenticated_user().id, receipt_no__created_at__month = 11, receipt_no__created_at__year=x.year)
#     total_sales_nov = 0
#     for nov_item in nov_items:
#         total_sales_nov += nov_item.get_sub_total()

#     dec_data = SRN.objects.filter(
#         user_id=get_current_authenticated_user().id, created_at__month = 12, created_at__year=x.year)
#     dec_items = SRI.objects.filter(receipt_no__user_id=get_current_authenticated_user().id, receipt_no__created_at__month = 12, receipt_no__created_at__year=x.year)
#     total_sales_dec = 0
#     for dec_item in dec_items:
#         total_sales_dec += dec_item.get_sub_total()

    return {
        'total_receipt': total_receipt.count(),
        'today_receipt': today_receipt.count(),
        'this_week': this_week.count(),
        'this_month': this_month.count(),

        # 'week_analysis_count': [sun_data.count(),mon_data.count(),tue_data.count(),
        #                     wed_data.count(),thur_data.count(),fri_data.count(),
        #                     sat_data.count()],
        
        # 'month_analysis_count':[
        #     jan_data.count(), feb_data.count(), mar_data.count(), apr_data.count(),
        #     may_data.count(),jun_data.count(), jul_data.count(), aug_data.count(),
        #     sep_data.count(), oct_data.count(),nov_data.count(), dec_data.count()
        # ],

        # 'month_analysis_sales': [
        #     total_sales_jan, total_sales_feb, total_sales_mar, total_sales_apr, total_sales_may, total_sales_jun,
        #     total_sales_jul, total_sales_aug, total_sales_sep, total_sales_oct, total_sales_nov, total_sales_dec,
        # ],
    }

