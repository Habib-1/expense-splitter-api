from decimal import Decimal
from .models import ExpenseShare,Group,GroupMembership,Expense
from django.shortcuts import get_object_or_404
from decimal import Decimal
from django.db.models import Sum
from .tasks import notify_expense_split
from silk.profiling.profiler import silk_profile
from django.contrib.auth import get_user_model
User=get_user_model()

@silk_profile(name="create_expense_share")
def create_expense_share(expense_id, amount, spliter_list):
    total_member = len(spliter_list)
    splited_amount = Decimal(amount) / Decimal(total_member)
    expense = Expense.objects.get(id=expense_id)

    obj_list=[ExpenseShare(expense_id=expense_id,user_id=user_id, share_amount=splited_amount) for user_id in spliter_list]

    ExpenseShare.objects.bulk_create(obj_list)

    email_map=dict(User.objects.filter(id__in=spliter_list).values_list('id','email'))
    for user_id in spliter_list:
        notify_expense_split.delay(
            email_map[user_id],
            expense.description,
            str(amount),
            str(splited_amount)
         )

  
def get_group(group_id):
    return get_object_or_404(Group,pk=group_id)

def get_group_members(group):
    return GroupMembership.objects.filter(group=group).select_related('user')

def get_group_expenses(group):
    return Expense.objects.filter(group=group)

def calculate_total_expense(expenses):
    return expenses.aggregate(total=Sum("amount"))["total"] or Decimal("0")



def calculate_member_financials(members, expenses, group):
    paid_map = dict(
        expenses.values('paid_by').annotate(total=Sum('amount'))
        .values_list('paid_by', 'total')
    )

    share_map = dict(
        ExpenseShare.objects.filter(expense__group=group)
        .values('user').annotate(total=Sum('share_amount'))
        .values_list('user', 'total')
    )

    member_financials = []
    for member in members:
        total_paid = paid_map.get(member.user_id) or Decimal("0")
        total_share = share_map.get(member.user_id) or Decimal("0")
        balance = total_paid - total_share

        member_financials.append({
            "user_id": member.user.id,
            "username": member.user.username,
            "paid": total_paid,
            "share": total_share,
            "balance": balance
        })

    return member_financials

def calculate_settlements(member_financials):
    debtors = []
    creditors = []

    for member in member_financials:
        if member["balance"] < 0:
            debtors.append({
                "username": member["username"],     
                "amount": abs(member["balance"]),
            })
        elif member["balance"] > 0:
            creditors.append({
                "username": member["username"],
                "amount": member["balance"],
            })

    settlements = []
    for debtor in debtors:
        for creditor in creditors:
            if debtor["amount"] == 0:
                break
            if creditor["amount"] == 0:
                continue    
            amount = min(debtor["amount"], creditor["amount"])
            settlements.append({
                "from": debtor["username"],
                "to": creditor["username"],
                "amount": amount,
            })
            debtor["amount"] -= amount
            creditor["amount"] -= amount
           

    return settlements

def get_group_summary(group_id):
    group = get_group(group_id)

    members = get_group_members(group)

    expenses = get_group_expenses(group)

    total_expense = calculate_total_expense(expenses)

    member_financials = calculate_member_financials(
        members,
        expenses,
        group
    )

    settlements = calculate_settlements(
        member_financials
    )

    return {
        "group": {
            "id": group.id,
            "name": group.name,
        },
        "total_expense": total_expense,
        "members": member_financials,
        "settlements": settlements,
    }
