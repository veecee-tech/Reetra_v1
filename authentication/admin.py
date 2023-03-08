
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import UserProfile

from .forms import UserAdminCreationForm, UserAdminChangeForm

User_Account = get_user_model()

# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ['username','number_count', 'is_admin', 'trial_version_exceeded']
    list_filter = ['trial_version_exceeded', 'email', 'phone']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email','phone')}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','trial_version_exceeded', 'password', 'password_2','is_staff','email', 'phone', 'is_admin', 'is_active')}
        ),
    )
    search_fields = ['username', 'email', 'phone']
    ordering = ['username']
    filter_horizontal = ()

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user','business_name', 'business_address', 'business_logo']


admin.site.register(User_Account, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)