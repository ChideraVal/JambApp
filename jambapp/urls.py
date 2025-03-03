from django.urls import path
from . import views

urlpatterns = [
    # path('quiz/', views.quiz),
    # path('cts/<int:transaction_id>/', views.check_transaction_status),
    path('', views.home),
    path('chapter1/', views.chapter1),
    path('chapter2/', views.chapter2),
    path('storecookie/<str:email>/<int:transaction_id>/', views.store_cookie),
    path('verify/', views.activate_order),
]
