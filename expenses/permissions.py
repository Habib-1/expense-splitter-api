from rest_framework.permissions import BasePermission
from .models import Group, GroupMembership

class IsGroupMember(BasePermission):
    message="Only group member can access data"

    def has_permission(self, request, view):
        group_id=view.kwargs.get('group_id')

        if not group_id:
            return False
        return GroupMembership.objects.filter(
            group=group_id,
            user=request.user
        ).exists()

        
class IsGroupAdmin(BasePermission):
    message="only admin can update, delete the expenses"

    def has_permission(self, request, view):
        group_id=view.kwargs.get("group_id")

        if not group_id:
            return False
        
        try:
            group=Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return False
       
        return group.created_by==request.user

