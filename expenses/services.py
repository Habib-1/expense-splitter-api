from decimal import Decimal
from .models import ExpenseShare,Group,GroupMembership,Expense
from django.shortcuts import get_object_or_404
from decimal import Decimal
from django.db.models import Sum

def create_expense_share(expense_id, amount, spliter_list):
    total_member = len(spliter_list)
    splited_amount = Decimal(amount) / Decimal(total_member)

    for user_id in spliter_list:
        ExpenseShare.objects.create(
            expense_id=expense_id,
            user_id=user_id,
            share_amount=splited_amount
        ) 



def get_group_summary(group_id):
    group=get_object_or_404(Group,pk=group_id)
    members=GroupMembership.objects.filter(group=group).select_related('user')
    expenses=Expense.objects.filter(group=group)
    total_expense=expenses.aggregate(
        total=Sum("amount")
     )["total"] or Decimal("0")


    member_paid={}

    for member in members:
        total_paid = expenses.filter(
            paid_by=member.user
        ).aggregate(
            total=Sum("amount")
        )["total"] or Decimal("0")

        member_paid[member.user.id] = total_paid

    member_share = {}

    for member in members:
        total_share = ExpenseShare.objects.filter(
            expense__group=group,
            user=member.user
        ).aggregate(
            total=Sum("share_amount")
        )["total"] or Decimal("0")

        member_share[member.user.id] = total_share

    member_balance = {}

    for member in members:
        user_id = member.user.id

        paid = member_paid.get(user_id, Decimal("0"))
        share = member_share.get(user_id, Decimal("0"))

        balance = paid - share

        member_balance[user_id] = balance

    debtors = []
    creditors = []

    for member in members:
        user_id = member.user.id
        balance = member_balance[user_id]

        if balance < 0:
            debtors.append({
                "user": member.user,
                "amount": abs(balance)
            })

        elif balance > 0:
            creditors.append({
                "user": member.user,
                "amount": balance
            })

    settlements = []

    for debtor in debtors:
        for creditor in creditors:

            amount = min(
                debtor["amount"],
                creditor["amount"]
            )

            settlements.append({
                "from": debtor["user"].username,
                "to": creditor["user"].username,
                "amount": amount,
            })

            debtor["amount"] -= amount
            creditor["amount"] -= amount

            if debtor["amount"] == 0:
                break

    member_data = []

    for member in members:
        user_id = member.user.id

        paid = member_paid.get(user_id, Decimal("0"))
        share = member_share.get(user_id, Decimal("0"))
        balance = member_balance.get(user_id, Decimal("0"))

        member_data.append({
            "username": member.user.username,
            "paid": paid,
            "share": share,
            "balance": balance,
        })

    return {
        "group": {
            "id": group.id,
            "name": group.name,
        },
        "total_expense": total_expense,
        "members": member_data,
        "settlements": settlements,
    }