from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.


admin.site.site_header = "Expense Splitter Admin"
admin.site.site_title = "Expense Splitter"
admin.site.index_title = "Welcome to Expense Splitter Administration"


class UserAdmin(BaseUserAdmin):
    ordering=['email']
    list_display=['username','email','first_name','last_name','is_staff','is_superuser']
    search_fields=['email','username']
    fieldsets=(
        (None,{'fields':('email','password')}),
        ("Personal Information" , {"fields":('username','first_name','last_name')}),
        ("Permission",{"fields":("is_staff","is_superuser")}),
    )
    add_fieldsets=(
        (None,{
            "classes": ("wide",),
            'fields':('username','email','password1','password2')}),
        ("Personal Info", {"classes": ("wide", "collapse"),"fields": ("first_name", "last_name")}),
    )


admin.site.register(CustomUser,UserAdmin)

