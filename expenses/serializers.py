from rest_framework import serializers
from . models import Group,GroupMembership



class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model=Group
        fields=('id','name','created_by','created_at')
        read_only_fields=('id','created_by','created_at')

class GroupMembershipSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = GroupMembership
        fields = ["id", "group", "user", "joined_at",]
        read_only_fields = ["id", "group", "joined_at"]
