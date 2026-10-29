import random

from django.contrib.auth.hashers import check_password, make_password
from django.db import models


class Account(models.Model):
    account_no = models.CharField(max_length=10, unique=True, editable=False)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=128)  # stored hashed, never plain text
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.account_no} - {self.name}"

    # ---- password helpers ----
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    # ---- account number generation ----
    @staticmethod
    def generate_account_no():
        while True:
            number = str(random.randint(1000000000, 9999999999))
            if not Account.objects.filter(account_no=number).exists():
                return number

    def save(self, *args, **kwargs):
        if not self.account_no:
            self.account_no = self.generate_account_no()
        super().save(*args, **kwargs)


class Transaction(models.Model):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"
    TRANSFER_OUT = "TRANSFER_OUT"
    TRANSFER_IN = "TRANSFER_IN"
    KIND_CHOICES = [
        (DEPOSIT, "Deposit"),
        (WITHDRAW, "Withdraw"),
        (TRANSFER_OUT, "Transfer Out"),
        (TRANSFER_IN, "Transfer In"),
    ]

    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="transactions"
    )
    kind = models.CharField(max_length=20, choices=KIND_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    balance_after = models.DecimalField(max_digits=12, decimal_places=2)
    note = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-id"]

    def __str__(self):
        return f"{self.kind} {self.amount} on {self.account.account_no}"
