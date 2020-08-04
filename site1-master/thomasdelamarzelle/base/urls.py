"""thomasdelamarzelle URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [

    path('', views.index, name='index'),
    path('logout', views.logoutpage, name='logout'),
    path('mydashboard', views.mydashboard, name='mydashboard'),
    path('register', views.register, name='register'),
    path('login', views.loginpage, name='login'),
    path('store', views.store, name='store'),
    path('student/<str:pk_test>/', views.student, name='student'),
    path('account_settings', views.account_settings, name='account_settings'),

    path('reset_password/' , auth_views.PasswordResetView.as_view(template_name="password_reset.html"), name='reset_password'),
    path('reset_password_sent/' , auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/' , auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/' , auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('cart', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout'),

    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name='process_order'),





]
