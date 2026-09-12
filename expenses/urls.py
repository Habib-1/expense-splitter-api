from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import GroupViewSet,AddMemberView
router=DefaultRouter()
router.register('group',GroupViewSet,basename='groupView')


urlpatterns = [
    path('', include(router.urls)),
    path(
        "groups/<int:group_id>/members/",
        AddMemberView.as_view(),
        name="add-member",
    ),
    
]
