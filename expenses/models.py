from django.db import models
from django.contrib.auth import get_user_model
User=get_user_model()

# Create your models here.
class Group(models.Model):
    name=models.CharField(max_length=500)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,related_name='created_groups')
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} Created by {self.created_by.username}'

class GroupMembership(models.Model):
    group=models.ForeignKey(Group,on_delete=models.CASCADE,related_name='membership')
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='group_membership')
    joined_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["group", "user"],
                name="unique_group_member",
            )
        ]
    def __str__(self):
        return f'{self.user} -- {self.group}'


# class Expense(models.Model):
#     pass



# class ExpenseShare(models.Model):
#     pass

