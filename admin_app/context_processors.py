# your_app/context_processors.py
from .models import Notification
from django.db.models import Sum 


def notification_count(request):
    print("Context processor is running...")
    contact_notification = Notification.objects.filter(notification_type='admin_contact_enquiry').first()
    admin_contact_enquiry_count = contact_notification.count if contact_notification else 0
    
    admin_order_count = Notification.objects.filter(notification_type='admin_order').first()
    admin_order_count = admin_order_count.count if admin_order_count else 0
    
    user_order_count = Notification.objects.filter(notification_type='user_order').first()
    user_order_count = user_order_count.count if user_order_count else 0
    
    user_cart_count = Notification.objects.filter(notification_type='user_cart').first()
    user_cart_count = user_cart_count.count if user_cart_count else 0
    
    return {
        'admin_contact_enquiry_count': admin_contact_enquiry_count,
        'admin_order_count' : admin_order_count,
        'user_order_count' : user_order_count,
        'user_cart_count' : user_cart_count,
    }