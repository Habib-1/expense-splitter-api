
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets,status
from rest_framework.views import APIView
from .serializers import GroupSerializer,GroupMembershipSerializer
from .models import Group,GroupMembership
from django.contrib.auth import get_user_model
User=get_user_model()
# Create your views here.


class GroupViewSet(viewsets.ModelViewSet):
    queryset=Group.objects.all()
    serializer_class=GroupSerializer
    permission_classes=[IsAuthenticated]


    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class AddMemberView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request,group_id):
        group=get_object_or_404(Group,pk=group_id)

        username=request.data.get('username')
        user=get_object_or_404(User,username=username)

        if GroupMembership.objects.filter(
            group=group,
            user=user
            ).exists():
                return Response(
                    {"detail": "This user is already a member of this group."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        
        membership=GroupMembership.objects.create(
            group=group,user=user
        )

        serializer=GroupMembershipSerializer(membership)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
