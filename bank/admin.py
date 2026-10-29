from django.contrib import admin

from .models import Account, Transaction


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("account_no", "name", "balance", "created_at")
    search_fields = ("account_no", "name")
    readonly_fields = ("account_no", "password", "created_at")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("account", "kind", "amount", "balance_after", "created_at")
    list_filter = ("kind",)
