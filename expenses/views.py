
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
        serializer.save(group=group,paid_by=self.request.user)

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes=[ IsAuthenticated,( IsGroupAdmin | IsExpenseOwner )]

        else :
            self.permission_classes=[IsAuthenticated,IsGroupMember]
        return [permission() for permission in self.permission_classes]

