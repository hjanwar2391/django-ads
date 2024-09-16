from django.contrib import admin
from .models import Withdrawal, Wallet
from django.utils.timezone import now, timedelta
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'withdrawal_method', 'status', 'created_at')
    list_filter = ('status', 'withdrawal_method', 'created_at')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        
        # Filter by day, week, or month using URL query params
        date_filter = request.GET.get('date_filter')
        
        if date_filter == 'today':
            queryset = queryset.filter(created_at__date=now().date())
        elif date_filter == 'this_week':
            start_of_week = now() - timedelta(days=now().weekday())
            queryset = queryset.filter(created_at__gte=start_of_week)
        elif date_filter == 'this_month':
            start_of_month = now().replace(day=1)
            queryset = queryset.filter(created_at__gte=start_of_month)

        return queryset

admin.site.register(Withdrawal, WithdrawalAdmin)

class AdminWallet(admin.ModelAdmin):
    list_display = ('user', 'points' )

admin.site.register(Wallet, AdminWallet)




class UserAdmin(BaseUserAdmin):
    # Specify the fields to display in the list view
    list_display = ('email', 'first_name', 'last_name', 'status', 'is_staff', 'is_superuser')
    list_filter = ('status', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    
    # Custom fields in the user change form
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone', 'address', 'city', 'zip_code', 'country')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'status')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Fields for the 'create user' form in the admin panel
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'phone', 'address', 'city', 'zip_code', 'country', 'is_active', 'is_staff', 'is_superuser', 'status'),
        }),
    )

    # Use email instead of username for identifying users
    add_form_template = 'admin/auth/user/add_form.html'
    search_help_text = 'Search by email, first name, or last name'

# Register the custom User model and the custom UserAdmin class
admin.site.register(User, UserAdmin)
