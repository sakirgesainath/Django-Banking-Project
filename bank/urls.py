from django.urls import path

from . import views

app_name = "bank"

urlpatterns = [
    path("", views.home, name="home"),
    path("new-account/", views.new_account, name="new_account"),
    path("balance/", views.view_balance, name="balance"),
    path("deposit/", views.deposit, name="deposit"),
    path("withdraw/", views.withdraw, name="withdraw"),
    path("transfer/", views.transfer, name="transfer"),
    path("close-account/", views.close_account, name="close_account"),
]
