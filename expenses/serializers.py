from rest_framework import serializers
from . models import Group,GroupMembership,Expense,ExpenseShare


class GroupMembershipSerializer(serializers.ModelSerializer):
    username=serializers.CharField(source='user.username',read_only=True)
    email=serializers.EmailField(source='user.email',read_only=True)
    group=serializers.CharField(source='group.name',read_only=True)
    class Meta:
        model = GroupMembership
        fields = ["id", "group", "username",'email', "joined_at",]
        read_only_fields = ["id", "group", "joined_at"]


class GroupSerializer(serializers.ModelSerializer):
    group_admin=serializers.CharField(source='created_by.username',read_only=True)
    members=GroupMembershipSerializer(many=True,source='membership')
    class Meta:
        model=Group
        fields=('id','name','group_admin','created_at','members')
        read_only_fields=('id','group_admin','created_at','members')


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Expense
        fields = [
            "id",
            "group",
            "paid_by",
            "amount",
            "description",
            "created_at",
        ]
        read_only_fields=['id','group','created_at']