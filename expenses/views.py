
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets,status
from rest_framework.views import APIView
from .serializers import GroupSerializer,GroupMembershipSerializer,ExpenseSerializer
from .models import Group,GroupMembership,Expense,ExpenseShare
from django.contrib.auth import get_user_model
User=get_user_model()
from .permissions import IsGroupAdmin,IsGroupMember
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
        serializer.save(group=group)

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes=[IsAuthenticated,IsGroupAdmin]

        else :
            self.permission_classes=[IsAuthenticated,IsGroupMember]
        return [permission() for permission in self.permission_classes]

