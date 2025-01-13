# your_app/context_processors.py
from .models import Notification

def notification_count(request):
    print("Context processor is running...")

    # Get the notification counts for the logged-in user
    user = request.user

    # Fetch notification count for different types
    admin_contact_notification = Notification.objects.filter(notification_type='admin_contact_enquiry').first()
    admin_contact_enquiry_count = admin_contact_notification.count if admin_contact_notification else 0
    
    admin_order_notification = Notification.objects.filter(notification_type='admin_order').first()
    admin_order_count = admin_order_notification.count if admin_order_notification else 0
    
    # Handle user-specific notifications (if authenticated)
    if user.is_authenticated:
        user_order_notification = Notification.objects.filter(notification_type='user_order', user=user).first()
        user_order_count = user_order_notification.count if user_order_notification else 0
        
        user_cart_notification = Notification.objects.filter(notification_type='user_cart', user=user).first()
        user_cart_count = user_cart_notification.count if user_cart_notification else 0
    else:
        # For unauthenticated users, set default values (or retain some notifications if needed)
        user_order_count = 0
        user_cart_count = 0

    # If there's an existing 'user_cart' notification for a non-logged-in user, consider showing it 
    # or preventing deletion after login.
    if not user.is_authenticated:
        cart_notification = Notification.objects.filter(notification_type='user_cart').first()
        user_cart_count = cart_notification.count if cart_notification else 0

    return {
        'admin_contact_enquiry_count': admin_contact_enquiry_count,
        'admin_order_count': admin_order_count,
        'user_order_count': user_order_count,
        'user_cart_count': user_cart_count,
    }
