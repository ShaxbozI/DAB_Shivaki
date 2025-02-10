from django.contrib import admin
from .models import (
    Bot_Users,
    Products,
    Type_Protucts,
    Type_Errors,
    SubType_Protucts,
    Manual_info,
    Qr_code,
)
from django.contrib.admin.models import LogEntry
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User



# Umumiy `has_change_permission` funksiyasi
def staff_active_permission(request, obj=None):
    """
    Faqat is_staff va is_active foydalanuvchilarga o'zgartirish imkoniyatini beradi.
    """
    return request.user.is_staff and request.user.is_active


class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('action_time', 'user', 'content_type', 'object_repr', 'action_flag', 'change_message')
    list_filter = ('action_time', 'user', 'content_type', 'action_flag')
    search_fields = ('object_repr', 'change_message')

# LogEntry'ni admin panelga qo‘shish
admin.site.register(LogEntry, LogEntryAdmin)



# Bot_Users admin
class Bot_UsersAdmin(admin.ModelAdmin):
    list_display = ('name', 'username', 'user_id', 'is_active', 'admin')
    list_filter = ('is_active', 'admin',)
    search_fields = ('name', 'username',)
    ordering = ('-create_at',)



# Products admin
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_type', 'product_sub_type', 'producing_now')
    list_filter = ('producing_now',)
    search_fields = ('name', 'product_type')
    ordering = ('-create_at',)



# Qr_code admin
class QrCodeAdmin(admin.ModelAdmin):
    fields = ['link_name', 'qr_file']
    
    def has_change_permission(self, request, obj=None):
        """
        Admin interfeysda obyektni yangilash imkoniyatini o'chirish.
        """
        return False  # Yangilashni taqiqlash

    def has_add_permission(self, request):
        """
        Qo'shish imkoniyatini saqlab qolish.
        """
        return True  # Qo'shishga ruxsat berish

    def has_delete_permission(self, request, obj=None):
        """
        O'chirish imkoniyatini boshqarish (kerak bo'lsa).
        """
        return True  # O'chirishga ruxsat berish

    def get_readonly_fields(self, request, obj=None):
        # Agar ob'ekt mavjud bo'lsa (tahrirlash yoki ko'rish), qo'shimcha maydonlarni ko'rsatamiz
        if obj:
            return ['link_name', 'qr_file', 'slug', 'qr_code_link', 'qr_code', 'create_at']
        # Yangi ob'ekt qo'shishda hech bir maydonni readonly qilmaymiz
        return []

    def get_fields(self, request, obj=None):
        # Agar ob'ekt mavjud bo'lsa, barcha maydonlarni ko'rsatamiz
        if obj:
            return ['link_name', 'qr_file', 'slug', 'qr_code_link', 'qr_code', 'create_at']
        # Aks holda, faqat kerakli maydonlarni ko'rsatamiz
        return ['link_name', 'qr_file']


# Custom User admin (superuser only)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active', 'is_superuser')
    list_filter = ('is_active', 'is_staff')
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)

    def has_change_permission(self, request, obj=None):
        """
        Faqat superuser o'zgartirish imkoniyatiga ega.
        """
        return request.user.is_superuser


# Admin registratsiyasi
admin.site.register(Bot_Users, Bot_UsersAdmin)
admin.site.register(Products, ProductsAdmin)
admin.site.register(Type_Protucts)
admin.site.register(Type_Errors)
admin.site.register(SubType_Protucts)
admin.site.register(Manual_info)
admin.site.register(Qr_code, QrCodeAdmin)

# User modelini qayta ro'yxatdan o'tkazish
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)









