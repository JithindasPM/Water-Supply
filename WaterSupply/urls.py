"""
URL configuration for WaterSupply project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

from app.views import Home_View
from app.views import Registration_View
from app.views import Login_View
from app.views import Admin_View
from app.views import User_View
from app.views import Product_Add_View
from app.views import Product_Update_View
from app.views import Product_Delete_View
from app.views import Update_UserProfile_View
from app.views import Customers_View
from app.views import Logout_View
from app.views import Order_Add_View
from app.views import Order_Update_View
from app.views import Order_Delete_View
from app.views import Shop_Product_View
from app.views import History_View
from app.views import Quick_Order_View
from app.views import Quick_Order_Update_View
from app.views import Quick_Order_Delete_View
from app.views import Admin_Order_View
from app.views import Admin_Quick_Order_View
from app.views import Admin_Order_Approval_View
from app.views import Admin_Quick_Order_Approval_View
from app.views import Payment_Success_View
from app.views import User_Billing_View
from app.views import Quick_Order_View, payment_success
from app.views import Bill_Order_View
from app.views import Bill_Quick_Order_View



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home_View.as_view(),name='home'),
    path('registration', Registration_View.as_view(),name='registration'),
    path('login', Login_View.as_view(),name='login'),
    path('admin', Admin_View.as_view(),name='admin'),
    path('user', User_View.as_view(),name='user'),
    path('product_add', Product_Add_View.as_view(),name='product_add'),
    path('product_update/<int:pk>', Product_Update_View.as_view(),name='product_update'),
    path('product_delete/<int:pk>', Product_Delete_View.as_view(),name='product_delete'),
    path('profile/<int:pk>', Update_UserProfile_View.as_view(),name='profile'),
    path('customers', Customers_View.as_view(),name='customers'),
    path('logout', Logout_View.as_view(),name='logout'),
    path('order_add', Order_Add_View.as_view(),name='order_add'),
    path('order_update/<int:pk>', Order_Update_View.as_view(),name='order_update'),
    path('order_delete/<int:pk>', Order_Delete_View.as_view(),name='order_delete'),
    path('shop_product', Shop_Product_View.as_view(),name='shop_product'),
    path('history', History_View.as_view(),name='history'),
    path('quick_order', Quick_Order_View.as_view(),name='quick_order'),
    path('quick_order_update/<int:pk>', Quick_Order_Update_View.as_view(),name='quick_order_update'),
    path('quick_order_delete/<int:pk>', Quick_Order_Delete_View.as_view(),name='quick_order_delete'),
    path('admin_order', Admin_Order_View.as_view(),name='admin_order'),
    path('admin_quick_order', Admin_Quick_Order_View.as_view(),name='admin_quick_order'),
    path('admin_order_update/<int:order_id>', Admin_Order_Approval_View.as_view(),name='admin_order_update'),
    path('admin_quick_order_update/<int:order_id>', Admin_Quick_Order_Approval_View.as_view(),name='admin_quick_order_update'),
    path('payment/success/', Payment_Success_View.as_view(), name='payment_success'),
    path('user_billing/', User_Billing_View.as_view(), name='user_billing'),
    path("payment-success/", payment_success, name="payment_successful"),
    path('bill_order/', Bill_Order_View.as_view(), name='bill_order'),
    path('bill_quick_order/', Bill_Quick_Order_View.as_view(), name='bill_quick_order'),
    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)