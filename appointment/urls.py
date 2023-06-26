from django.urls import path

from appointment import views

app_name = 'appointment'
urlpatterns = [
    path('my-appointment/', views.my_appointment, name='my_appointment'),
    path('book-appointment/', views.book_a_appointment, name='book_a_appointment')
]
