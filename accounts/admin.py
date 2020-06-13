from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Buyer, Seller


from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import GuestEmail, EmailActivation

User = get_user_model()



class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'admin')
    list_filter = ('admin', 'staff', 'is_active','is_seller')
    fieldsets = (
        (None, {'fields': ('full_name', 'email', 'password')}),
       # ('Full name', {'fields': ()}),
        ('Permissions', {'fields': ('admin', 'staff', 'is_active','is_seller',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',
                'staff', 'is_superuser', 'is_seller',)}
        ),
    )
    search_fields = ('email', 'full_name',)
    ordering = ('email',)
    filter_horizontal = ()
    readonly_fields = ('id', 'timestamp',)

admin.site.register(User, UserAdmin)

# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)



class EmailActivationAdmin(admin.ModelAdmin):
    search_fields = ['email']
    class Meta:
        model = EmailActivation


admin.site.register(EmailActivation, EmailActivationAdmin)


class GuestEmailAdmin(admin.ModelAdmin):
    search_fields = ['email']
    class Meta:
        model = GuestEmail



class BuyerAdmin(admin.ModelAdmin):
    list_display = ('id',)
    readonly_fields = ('id',)


class SellerAdmin(admin.ModelAdmin):
    list_display = ('id', 'stripe_user_id', 'stripe_access_token',)
    readonly_fields = ('id',)




admin.site.register(Buyer, BuyerAdmin)
admin.site.register(Seller, SellerAdmin)


admin.site.register(GuestEmail, GuestEmailAdmin)