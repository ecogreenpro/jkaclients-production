from django.urls import path

from service import views

app_name = 'service'
urlpatterns = [
    path('my-service/', views.my_service, name='my-service'),
    path('contract/', views.contract, name='contract'),
    path('document/', views.my_documents, name='my_document'),
    path('upolad/<contract_id>/', views.upload_file, name='upload_file')
]
