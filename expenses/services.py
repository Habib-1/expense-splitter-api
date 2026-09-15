from decimal import Decimal
from .models import ExpenseShare

def create_expense_share(expense_id, amount, spliter_list):
    total_member = len(spliter_list)
    splited_amount = Decimal(amount) / Decimal(total_member)

    for user_id in spliter_list:
        ExpenseShare.objects.create(
            expense_id=expense_id,
            user_id=user_id,
            share_amount=splited_amount
        ) 

