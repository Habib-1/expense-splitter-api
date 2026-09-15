
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets,status,generics
from rest_framework.views import APIView
from .serializers import GroupSerializer,GroupMembershipSerializer,ExpenseSerializer
from .models import Group,GroupMembership,Expense,ExpenseShare
from django.contrib.auth import get_user_model
User=get_user_model()
from .permissions import IsGroupAdmin,IsGroupMember,IsExpenseOwner
from .services import create_expense_share
# Create your views here.


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class=GroupSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return Group.objects.filter(membership__user=self.request.user).distinct()

    def perform_create(self, serializer):
        group=serializer.save(created_by=self.request.user)
        GroupMembership.objects.create(
            group=group,
            user=self.request.user
        )

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes=[IsAuthenticated,IsGroupAdmin]
        else :
            self.permission_classes=[IsAuthenticated]

        return [permission() for permission in self.permission_classes]


class AddMemberView(generics.CreateAPIView):
    queryset=GroupMembership.objects.all()
    serializer_class=GroupMembershipSerializer
    permission_classes=[IsAuthenticated,IsGroupAdmin]

    def perform_create(self, serializer):

        group_id=self.kwargs["group_id"]
        group=get_object_or_404(Group,id=group_id)

        username=self.request.data.get('username')
        user=get_object_or_404(User,username=username)

        if GroupMembership.objects.filter(group=group, user=user).exists():
            raise ValidationError("This user is already a member of this group.")

        serializer.save(group=group,user=user)


class RemoveMemberView(generics.DestroyAPIView):
    serializer_class=GroupMembershipSerializer
    permission_classes=[IsAuthenticated,IsGroupAdmin]

    def get_queryset(self):
        group_id=self.kwargs["group_id"]
        member=GroupMembership.objects.filter(group=group_id)
        return member



class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class=ExpenseSerializer

    def get_queryset(self):
        group_id=self.kwargs['group_id']

        return Expense.objects.filter(group=group_id)

    def perform_create(self, serializer):
        group_id=self.kwargs["group_id"]
        group = get_object_or_404(
            Group,
            id=group_id
            )
        
        spliter_list = serializer.validated_data.pop('splitter_list', None)

        expense=serializer.save(group=group,paid_by=self.request.user)

        if not spliter_list:
            spliter_list = list(
                GroupMembership.objects.filter(group=group).values_list('user_id', flat=True)
            )
        create_expense_share(
            expense_id=expense.id,
            amount=expense.amount,
            spliter_list=spliter_list
            )

    def perform_update(self, serializer):
        expense = self.get_object()
        old_amount = expense.amount

        splitter_list = serializer.validated_data.pop('splitter_list', None)
        updated_expense = serializer.save()


        if splitter_list or updated_expense.amount != old_amount:
            if not splitter_list:
                splitter_list = list(
                    updated_expense.shares.values_list('user_id', flat=True)
                )
            updated_expense.shares.all().delete()
            create_expense_share(
                expense_id=updated_expense.id,
                amount=updated_expense.amount,
                spliter_list=splitter_list
            )


    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes=[ IsAuthenticated,( IsGroupAdmin | IsExpenseOwner )]

        else :
            self.permission_classes=[IsAuthenticated,IsGroupMember]
        return [permission() for permission in self.permission_classes]

