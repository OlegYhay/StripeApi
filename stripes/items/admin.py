from django.contrib import admin

# Register your models here.
from .models import Items, Order, Discount, Tax


@admin.register(Items)
class ItemsAdminView(admin.ModelAdmin):
    pass

@admin.register(Order)
class OrderAdminView(admin.ModelAdmin):
    pass

@admin.register(Discount)
class OrderAdminView(admin.ModelAdmin):
    pass

@admin.register(Tax)
class OrderAdminView(admin.ModelAdmin):
    pass