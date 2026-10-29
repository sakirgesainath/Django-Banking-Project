from django.db import transaction
from django.shortcuts import render

from .forms import (
    BalanceForm,
    CloseAccountForm,
    DepositForm,
    NewAccountForm,
    TransferForm,
    WithdrawForm,
)
from .models import Account, Transaction


def home(request):
    return render(request, "bank/home.html")


def new_account(request):
    form = NewAccountForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
        initial = data.get("initial_deposit") or 0
        with transaction.atomic():
            account = Account(name=data["name"].strip(), balance=initial)
            account.set_password(data["password"])
            account.save()
            if initial > 0:
                Transaction.objects.create(
                    account=account,
                    kind=Transaction.DEPOSIT,
                    amount=initial,
                    balance_after=account.balance,
                    note="Initial deposit",
                )
        return render(
            request,
            "bank/result.html",
            {
                "title": "Account Created",
                "message": "Your account has been created successfully. "
                "Please note your account number.",
                "account": account,
            },
        )
    return render(request, "bank/new_account.html", {"form": form})


def view_balance(request):
    form = BalanceForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        account = form.account
        return render(
            request,
            "bank/result.html",
            {
                "title": "Account Balance",
                "message": f"Welcome, {account.name}.",
                "account": account,
                "transactions": account.transactions.all()[:10],
            },
        )
    return render(request, "bank/balance.html", {"form": form})


def deposit(request):
    form = DepositForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        amount = form.cleaned_data["amount"]
        with transaction.atomic():
            account = Account.objects.select_for_update().get(pk=form.account.pk)
            account.balance += amount
            account.save(update_fields=["balance"])
            Transaction.objects.create(
                account=account,
                kind=Transaction.DEPOSIT,
                amount=amount,
                balance_after=account.balance,
            )
        return render(
            request,
            "bank/result.html",
            {
                "title": "Deposit Successful",
                "message": f"₹{amount} has been deposited.",
                "account": account,
            },
        )
    return render(request, "bank/deposit.html", {"form": form})


def withdraw(request):
    form = WithdrawForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        amount = form.cleaned_data["amount"]
        with transaction.atomic():
            account = Account.objects.select_for_update().get(pk=form.account.pk)
            if amount > account.balance:  # re-check on the locked row
                form.add_error(None, "Insufficient balance for this withdrawal.")
                return render(request, "bank/withdraw.html", {"form": form})
            account.balance -= amount
            account.save(update_fields=["balance"])
            Transaction.objects.create(
                account=account,
                kind=Transaction.WITHDRAW,
                amount=amount,
                balance_after=account.balance,
            )
        return render(
            request,
            "bank/result.html",
            {
                "title": "Withdrawal Successful",
                "message": f"₹{amount} has been withdrawn.",
                "account": account,
            },
        )
    return render(request, "bank/withdraw.html", {"form": form})


def transfer(request):
    form = TransferForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        amount = form.cleaned_data["amount"]
        with transaction.atomic():
            # lock both rows in a fixed order to avoid deadlocks
            locked = {
                a.pk: a
                for a in Account.objects.select_for_update()
                .filter(pk__in=[form.account.pk, form.receiver.pk])
                .order_by("pk")
            }
            sender = locked[form.account.pk]
            receiver = locked[form.receiver.pk]
            if amount > sender.balance:
                form.add_error(None, "Insufficient balance for this transfer.")
                return render(request, "bank/transfer.html", {"form": form})
            sender.balance -= amount
            receiver.balance += amount
            sender.save(update_fields=["balance"])
            receiver.save(update_fields=["balance"])
            Transaction.objects.create(
                account=sender,
                kind=Transaction.TRANSFER_OUT,
                amount=amount,
                balance_after=sender.balance,
                note=f"To {receiver.account_no}",
            )
            Transaction.objects.create(
                account=receiver,
                kind=Transaction.TRANSFER_IN,
                amount=amount,
                balance_after=receiver.balance,
                note=f"From {sender.account_no}",
            )
        return render(
            request,
            "bank/result.html",
            {
                "title": "Transfer Successful",
                "message": f"₹{amount} transferred to account {receiver.account_no}.",
                "account": sender,
            },
        )
    return render(request, "bank/transfer.html", {"form": form})


def close_account(request):
    form = CloseAccountForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        account = form.account
        name, number, balance = account.name, account.account_no, account.balance
        account.delete()
        return render(
            request,
            "bank/result.html",
            {
                "title": "Account Closed",
                "message": f"Account {number} of {name} has been closed. "
                f"Please collect your remaining balance of ₹{balance} from the branch.",
            },
        )
    return render(request, "bank/close_account.html", {"form": form})
