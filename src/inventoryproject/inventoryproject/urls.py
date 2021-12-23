"""inventoryproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from main.views import *
urlpatterns = [
    path('',homePage,name="homePage"),
    path('index',homePage,name='homePage'),
    
    path('sell',sell,name="sell"),
    path('admins',admins,name="admins"),
    path('supplier',supplier,name="supplier"),
    path('purchase',purchase,name="purchase"),
    path('register',register,name="register"),
    path('addsup',addsup,name="addsup"),
    path('login',login,name="login"),
    path('admin/', admin.site.urls),
]
