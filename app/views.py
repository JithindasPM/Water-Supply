from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import View
from django.contrib.auth import login,logout,authenticate
from django.core.paginator import Paginator


# Create your views here.

from app.models import User
from app.models import UserProfile_Model
from app.models import Product
from app.models import Order
from app.models import Quick_Order

from app.forms import Registration_Form
from app.forms import Login_Form
from app.forms import Product_Form
from app.forms import UserProfile_Form
from app.forms import Order_Form
from app.forms import Quick_Order_Form


class Home_View(View):
    def get(self,request,*args,**kwargs):
        return render(request,'index.html')
    

class Registration_View(View):
    def get(self,request,*args,**kwargs):
        form=Registration_Form()
        return render(request,'reg.html',{'form':form})
    
    def post(self,request,*args,**kwargs):
        form=Registration_Form(request.POST)
        try:
            if form.is_valid():
               User.objects.create_user(**form.cleaned_data)
               form=Registration_Form()
               return redirect('login')
        except Exception as e:
            print(e,"===========")
        return render(request,'reg.html',{'form':form})
        
class Update_UserProfile_View(View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        data=UserProfile_Model.objects.get(id=id)
        form = UserProfile_Form(instance=data)
        return render(request, 'profile.html', {'form': form,'data':data})
    
    def post(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        data=UserProfile_Model.objects.get(id=id)
        form = UserProfile_Form(request.POST, instance=data)
        if form.is_valid():
            form.save()
            if request.user.is_superuser:
                return redirect('admin')  # Redirect to 'admin' if superuser
            else:
                return redirect('user')  # Redirect to 'user' otherwise

        return render(request, 'profile.html', {'form': form, 'data': data})

class Login_View(View):
    def get(self,request):
        form=Login_Form()
        return render(request,'login.html',{'form':form})
    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user) 
            if user.is_superuser: 
                return redirect("admin") 
            else:
                return redirect("user") 
        form=Login_Form()
        return render(request, "login.html", {"error": "Invalid credentials",'form':form})
    
class Logout_View(View):
    def get(self, request):
        logout(request)
        return redirect('home')
    

class Admin_View(View):
    def get(self,request,*args,**kwargs):
        return render(request,'admin.html')
    
class User_View(View):
    def get(self,request,*args,**kwargs):
        orders_list = Order.objects.filter(customer=request.user).order_by('-id')[:5]
        total_orders = Order.objects.filter(customer=request.user).count()
        successful_deliveries = Order.objects.filter(customer=request.user, status="Delivered").count()
        upcoming_deliveries = Order.objects.filter(customer=request.user, status__in=["Requested", "Pending"]).count()
        return render(request,'user.html',{'orders_list':orders_list,'successful_deliveries':successful_deliveries,
                                           'total_orders':total_orders,'upcoming_deliveries':upcoming_deliveries})
    

# Products -----------------------------------


class Product_Add_View(View):
    def get(self, request):
        form = Product_Form()
        products = Product.objects.all()
        return render(request, 'product.html', {'form': form,'products': products})

    def post(self, request):
        products = Product.objects.all()
        form = Product_Form(request.POST)
        if form.is_valid():
            form.save()
        form = Product_Form()
        return render(request, 'product.html', {'form': form,'products': products})


class Product_Update_View(View):
    def get(self, request,**kwargs):
        products = Product.objects.all()
        pk=kwargs.get('pk')
        product = get_object_or_404(Product, pk=pk)
        form = Product_Form(instance=product)
        return render(request, 'product.html', {'form': form,'products': products})

    def post(self, request, **kwargs):
        products = Product.objects.all()
        pk=kwargs.get('pk')
        product = get_object_or_404(Product, pk=pk)
        form = Product_Form(request.POST, instance=product)
        if form.is_valid():
            form.save()
            form = Product_Form()
        return redirect('product_add')


class Product_Delete_View(View):
    def get(self, request, **kwargs):
        pk=kwargs.get('pk')
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return redirect('product_add')

# Products -----------------------------------


class Customers_View(View):
    def get(self, request, **kwargs):
        customers = UserProfile_Model.objects.filter(user__is_superuser=False)
        return render(request, 'customers.html', {'customers': customers})
    

class History_View(View):
    def get(self, request):
        orders_list = Order.objects.filter(customer=request.user).order_by('-id')
        
        # Pagination: 10 orders per page
        paginator = Paginator(orders_list, 10)
        page_number = request.GET.get('page')
        orders = paginator.get_page(page_number)

        return render(request, 'history.html', {'orders': orders})

class Order_Add_View(View):
    def get(self, request):
        form = Order_Form()
        orders_list = Order.objects.filter(customer=request.user).order_by('-id')
        
        paginator = Paginator(orders_list, 10)
        page_number = request.GET.get('page')
        orders = paginator.get_page(page_number)

        return render(request, 'order.html', {'form': form, 'orders': orders})

    def post(self, request):
        orders_list = Order.objects.filter(customer=request.user).order_by('-id')
        form = Order_Form(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            order.customer = request.user 
            order.save()
        form = Order_Form()

        paginator = Paginator(orders_list, 10)
        page_number = request.GET.get('page')
        orders = paginator.get_page(page_number)

        return render(request, 'order.html', {'form': form, 'orders': orders})


class Order_Update_View(View):
    def get(self, request, **kwargs):
        pk=kwargs.get('pk')
        data = get_object_or_404(Order, id=pk, customer=request.user)
        form = Order_Form(instance=data)
        order=Order.objects.filter(customer=request.user)
        return render(request, 'order.html', {'form': form,'order':order})

    def post(self, request, **kwargs):
        pk=kwargs.get('pk')
        data = get_object_or_404(Order, id=pk, customer=request.user)
        form = Order_Form(request.POST, instance=data)
        if form.is_valid():
            form.save()
            form = Order_Form()
            order=Order.objects.filter(customer=request.user)
        return render(request, 'order.html', {'form': form,'order':order})


class Admin_Order_Approval_View(View):
    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        if request.user.is_superuser: 
            status = request.POST.get('status')
            if status in dict(Order.STATUS_CHOICES).keys():
                order.status = status
                order.save()
        else:
            return redirect('admin_order') 
        return redirect('admin_order')  

    
class Order_Delete_View(View):
    def get(self, request, **kwargs):
        pk=kwargs.get('pk')
        data = get_object_or_404(Order, id=pk, customer=request.user)
        data.delete()
        return redirect('order_add')
    

class Shop_Product_View(View):
    def get(self, request, **kwargs):
        product=Product.objects.all()
        return render(request, 'shop_product.html',{'product':product})


#   quick order==============================


class Quick_Order_View(View):
    def get(self, request, *args, **kwargs):
        form = Quick_Order_Form()
        orders = Quick_Order.objects.filter(customer=request.user).order_by('-id')
        
        # Pagination setup: 5 orders per page (change as needed)
        paginator = Paginator(orders, 5)  
        page_number = request.GET.get('page')
        page_orders = paginator.get_page(page_number)

        return render(request, 'quick_order.html', {'form': form, 'orders': page_orders})

    def post(self, request, *args, **kwargs):
        orders = Quick_Order.objects.filter(customer=request.user).order_by('-id')
        
        form = Quick_Order_Form(request.POST)
        if form.is_valid():
            quick_order = form.save(commit=False)
            quick_order.customer = request.user
            quick_order.save()
            form = Quick_Order_Form()

        # Pagination setup
        paginator = Paginator(orders, 5)  
        page_number = request.GET.get('page')
        page_orders = paginator.get_page(page_number)

        return render(request, 'quick_order.html', {'form': form, 'orders': page_orders})
    
class Quick_Order_Update_View(View):
    def get(self, request, *args, **kwargs):
        pk=kwargs.get('pk')
        order = get_object_or_404(Quick_Order, id=pk, customer=request.user)
        form = Quick_Order_Form(instance=order)
        orders=Quick_Order.objects.filter(customer=request.user).order_by('-id')
        return render(request, 'quick_order.html', {'form': form, 'order': order,'orders':orders})

    def post(self, request, *args, **kwargs):
        pk=kwargs.get('pk')
        order = get_object_or_404(Quick_Order, id=pk, customer=request.user)
        form = Quick_Order_Form(request.POST, instance=order)
        if form.is_valid():
            form.save()
            orders=Quick_Order.objects.filter(customer=request.user).order_by('-id')
            return redirect('quick_order')
        return render(request, 'quick_order.html', {'form': form, 'order': order,'orders':orders})
    

class Admin_Quick_Order_Approval_View(View):
    def post(self, request, order_id):
        order = get_object_or_404(Quick_Order, id=order_id)
        if request.user.is_superuser: 
            status = request.POST.get('status')
            if status in dict(Order.STATUS_CHOICES).keys():
                order.status = status
                order.save()
        else:
            return redirect('admin_quick_order') 
        return redirect('admin_quick_order')  

    
class Quick_Order_Delete_View(View):
    def get(self, request, *args, **kwargs):
        pk=kwargs.get('pk')
        order = Quick_Order.objects.get(id=pk)
        order.delete()
        return redirect('quick_order') 

class Admin_Order_View(View):
    def get(self, request, *args, **kwargs):
        orders = Order.objects.all().order_by('-id')

        # Pagination setup: Show 10 orders per page
        paginator = Paginator(orders, 10)
        page_number = request.GET.get('page')
        page_orders = paginator.get_page(page_number)

        return render(request, 'admin_order.html', {'orders': page_orders})

class Admin_Quick_Order_View(View):
    def get(self, request, *args, **kwargs):
        orders = Quick_Order.objects.all().order_by('-id')

        # Pagination setup: Show 10 orders per page
        paginator = Paginator(orders, 10)
        page_number = request.GET.get('page')
        page_orders = paginator.get_page(page_number)

        return render(request, 'admin_quick_order.html', {'orders': page_orders})


    



