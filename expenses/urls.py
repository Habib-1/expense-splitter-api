from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import GroupViewSet,AddMemberView,ExpenseViewSet,RemoveMemberView
router=DefaultRouter()
router.register('groups',GroupViewSet,basename='groups')


urlpatterns = [
    path('', include(router.urls)),

    path(
        "groups/<int:group_id>/members/",
        AddMemberView.as_view(),
        name="add-member",
    ),
    path(
        "groups/<int:group_id>/members/<int:pk>/",
        RemoveMemberView.as_view(),
        name="group-member-delete"
    ),
    path(
        'groups/<int:group_id>/expenses/'
        ,ExpenseViewSet.as_view(
           { 
            "get":"list",
            "post":"create"
            }
        ),
        name="expense-list-create"
        ),

    path(
        "groups/<int:group_id>/expenses/<int:pk>/",
         ExpenseViewSet.as_view(
            {
                "get":"retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="expenses-details"
        ),

    
]
