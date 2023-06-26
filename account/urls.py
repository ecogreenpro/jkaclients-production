from django.urls import path

from account import views

app_name = 'account'
urlpatterns = [
    path('invoice/', views.invoice, name='invoice'),
    path('payment/', views.payment, name='payment')
]
