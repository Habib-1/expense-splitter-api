from celery import shared_task
from django.core.mail import send_mail


@shared_task
def notify_added_to_group(user_email, group_name):
    send_mail(
        subject=f"তোমাকে '{group_name}' গ্রুপে যোগ করা হয়েছে",
        message=f"তুমি এখন '{group_name}' গ্রুপের সদস্য।",
        from_email=None,  # DEFAULT_FROM_EMAIL settings.py theke nibe
        recipient_list=[user_email],
    )


@shared_task
def notify_expense_split(user_email, expense_title, amount, split_amount):
    send_mail(
        subject=f"নতুন expense হয়েছে: {expense_title}",
        message=(
            f"'{expense_title}' নামে {amount} টাকার একটা expense তৈরি হয়েছে, "
            f"যেখানে তোমার share হলো {split_amount} টাকা।"
        ),
        from_email=None,
        recipient_list=[user_email],
    )