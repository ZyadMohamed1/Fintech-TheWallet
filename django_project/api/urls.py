from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('payments/', views.getPayments),
    path('payments/create/', views.createPayment),
    path('payments/<str:pk>/update/', views.updatePayment),
    path('payments/<str:pk>/delete/', views.deletePayment),
    path('payments/<str:pk>/', views.getPayment)
]