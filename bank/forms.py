from decimal import Decimal

from django import forms
from django.core.exceptions import ValidationError

from .models import Account

AMOUNT_MIN = Decimal("0.01")


class NewAccountForm(forms.Form):
    name = forms.CharField(max_length=100, label="Full Name")
    password = forms.CharField(
        min_length=4, widget=forms.PasswordInput, label="Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput, label="Confirm Password"
    )
    initial_deposit = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=Decimal("0"),
        initial=0,
        label="Initial Deposit (optional)",
        required=False,
    )

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password") and cleaned.get("confirm_password"):
            if cleaned["password"] != cleaned["confirm_password"]:
                self.add_error("confirm_password", "Passwords do not match.")
        return cleaned


class AccountAuthForm(forms.Form):
    """Base form: validates account no + name + password together."""

    account_no = forms.CharField(max_length=10, label="Account Number")
    name = forms.CharField(max_length=100, label="Account Holder Name")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    account = None  # set after successful validation

    def clean(self):
        cleaned = super().clean()
        account_no = cleaned.get("account_no")
        name = cleaned.get("name")
        password = cleaned.get("password")
        if account_no and name and password:
            account = Account.objects.filter(account_no=account_no.strip()).first()
            if (
                account is None
                or account.name.strip().lower() != name.strip().lower()
                or not account.check_password(password)
            ):
                raise ValidationError(
                    "Invalid account number, name or password. Please try again."
                )
            self.account = account
        return cleaned


class AmountMixin(forms.Form):
    amount = forms.DecimalField(
        max_digits=12, decimal_places=2, min_value=AMOUNT_MIN, label="Amount"
    )


class BalanceForm(AccountAuthForm):
    pass


class DepositForm(AmountMixin, AccountAuthForm):
    pass


class WithdrawForm(AmountMixin, AccountAuthForm):
    def clean(self):
        cleaned = super().clean()
        amount = cleaned.get("amount")
        if self.account and amount and amount > self.account.balance:
            raise ValidationError("Insufficient balance for this withdrawal.")
        return cleaned


class TransferForm(AmountMixin, AccountAuthForm):
    field_order = ["account_no", "name", "password", "to_account_no", "amount"]

    to_account_no = forms.CharField(max_length=10, label="Receiver Account Number")

    receiver = None

    def clean(self):
        cleaned = super().clean()
        to_no = cleaned.get("to_account_no")
        amount = cleaned.get("amount")
        if self.account and to_no:
            if to_no.strip() == self.account.account_no:
                raise ValidationError("You cannot transfer money to your own account.")
            self.receiver = Account.objects.filter(account_no=to_no.strip()).first()
            if self.receiver is None:
                self.add_error("to_account_no", "Receiver account does not exist.")
            elif amount and amount > self.account.balance:
                raise ValidationError("Insufficient balance for this transfer.")
        return cleaned


class CloseAccountForm(AccountAuthForm):
    confirm = forms.BooleanField(
        label="I understand this will permanently close my account"
    )
