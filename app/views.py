from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import View
from django.contrib.auth import login,logout,authenticate
from django.core.paginator import Paginator

import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.db.models import Sum 


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
    def get(self, request, *args, **kwargs):
        form = Registration_Form()
        return render(request, 'reg.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = Registration_Form(request.POST)
        try:
            if form.is_valid():
                cleaned_data = form.cleaned_data
                cleaned_data.pop('confirm_password')  # Remove confirm_password

                User.objects.create_user(**cleaned_data)  # Create user
                return redirect('login')
        except Exception as e:
            print(e, "===========")
        
        return render(request, 'reg.html', {'form': form})

        
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
    
    
from django.db.models import Sum
from django.utils.timezone import now
from datetime import date

class Admin_View(View):
    def get(self,request,*args,**kwargs):
        
        today = date.today()
        current_month = today.month
        current_year = today.year
        
        # Calculate total from Order model
        order_total = Order.objects.filter(
            is_paid=True, 
            order_date__year=current_year, 
            order_date__month=current_month
        ).aggregate(Sum('total_price'))['total_price__sum'] or 0

        # Calculate total from Quick_Order model
        quick_order_total = Quick_Order.objects.filter(
            is_paid=True, 
            order_date__year=current_year, 
            order_date__month=current_month
        ).aggregate(Sum('total_price'))['total_price__sum'] or 0

        # Total amount from both models
        total_amount = order_total + quick_order_total

    
        data = Order.objects.all().order_by('-id')[:3]
        all_orders=Order.objects.all().count()
        all_quick=Quick_Order.objects.all().count()
        user_count = User.objects.filter(is_superuser=False).count()
        return render(request,'admin.html',{'data':data,'all_orders':all_orders,'all_quick':all_quick,
                                            'user_count':user_count,'total_amount':total_amount})
  

class User_View(View):
    def get(self,request,*args,**kwargs):
        orders_list = Order.objects.filter(customer=request.user).order_by('-id')[:4]
        total_orders = Order.objects.filter(customer=request.user).count()
        successful_deliveries = Order.objects.filter(customer=request.user, status="Delivered").count()
        upcoming_deliveries = Order.objects.filter(customer=request.user, status__in=["Requested", "Pending"]).count()
        total_spent = Order.objects.filter(customer=request.user, is_paid=True).aggregate(total_amount=Sum('total_price'))['total_amount'] or 0
        return render(request,'user.html',{'orders_list':orders_list,'successful_deliveries':successful_deliveries,
                                           'total_orders':total_orders,'upcoming_deliveries':upcoming_deliveries,
                                           'total_spent':total_spent})
    

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


from django.utils import timezone

from django.views import View
from django.shortcuts import render, redirect
from .forms import Order_Form
import razorpay
from django.conf import settings

class Order_Add_View(View):
    def get(self, request):
        form = Order_Form()
        orders_list = Order.objects.filter(customer=request.user).order_by('-id')

        paginator = Paginator(orders_list, 10)
        page_number = request.GET.get('page')
        orders = paginator.get_page(page_number)

        return render(request, 'order.html', {'form': form, 'orders': orders})

    def post(self, request):
        form = Order_Form(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            order.customer = request.user

            total_price = float(order.product.price * order.quantity)  # Convert Decimal to float
            amount_in_paise = int(total_price * 100)  # Convert rupees to paise

            # ✅ Create Razorpay order
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            payment = client.order.create({
                "amount": amount_in_paise,  # Paise
                "currency": "INR",
                "payment_capture": 1
            })

            request.session['order_data'] = {
                'product_id': order.product.id,
                'quantity': order.quantity,
                'total_price': total_price,
                'order_date': str(order.order_date)  
            }
            request.session['razorpay_order_id'] = payment['id']

            return render(request, 'payment.html', {
                'razorpay_key_id': settings.RAZORPAY_KEY_ID,
                'amount': total_price, 
                'order_id': payment['id'] 
            })

        return render(request, 'order.html', {'form': form})



@method_decorator(csrf_exempt, name='dispatch')
class Payment_Success_View(View):
    def post(self, request):
        data = request.POST
        razorpay_order_id = data.get('razorpay_order_id')

        order_data = request.session.get('order_data')

        if not order_data or razorpay_order_id != request.session.get('razorpay_order_id'):
            print("Order data mismatch or missing session data")  
            return redirect('user')  

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': data.get('razorpay_payment_id'),
                'razorpay_signature': data.get('razorpay_signature')
            })

            order = Order(
                customer=request.user,
                product=Product.objects.get(id=order_data['product_id']),
                quantity=order_data['quantity'],
                total_price=order_data['total_price'],
                order_date=timezone.now(),
                razorpay_order_id=razorpay_order_id,
                razorpay_payment_id=data.get('razorpay_payment_id'),
                razorpay_signature=data.get('razorpay_signature'),
                is_paid=True
            )
            order.save()

            print("✅ Order saved successfully!") 

            del request.session['order_data']
            del request.session['razorpay_order_id']

            return redirect('user')  
        
        except razorpay.errors.SignatureVerificationError:
            print("❌ Signature verification failed!")  
            return redirect('user') 

       
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


class User_Billing_View(View):
    def get(self, request, *args, **kwargs):
        return render(request,'order_bill.html')

import razorpay
from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from .models import Quick_Order
from .forms import Quick_Order_Form

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View
from decimal import Decimal

class Quick_Order_View(View):
    def get(self, request, *args, **kwargs):
        form = Quick_Order_Form()
        orders = Quick_Order.objects.filter(customer=request.user).order_by('-id')

        paginator = Paginator(orders, 5)
        page_number = request.GET.get('page')
        page_orders = paginator.get_page(page_number)

        return render(request, 'quick_order.html', {'form': form, 'orders': page_orders})

    def post(self, request, *args, **kwargs):
        form = Quick_Order_Form(request.POST)
        if form.is_valid():
            product = form.cleaned_data.get("product")
            quantity = form.cleaned_data.get("quantity")

            total_price = float(product.price * quantity)

            request.session["quick_order_data"] = {
                "product_id": product.id,
                "quantity": quantity,
                "order_date": str(form.cleaned_data.get("order_date")),
                "location_url": form.cleaned_data.get("location_url"),
                "total_price": total_price,
            }

            razorpay_order = razorpay_client.order.create({
                "amount": int(total_price * 100), 
                "currency": "INR",
                "payment_capture": "1",
            })

            request.session["razorpay_order_id"] = razorpay_order["id"]

            return render(
                request,
                "payment_page.html",
                {
                    "razorpay_order_id": razorpay_order["id"],
                    "razorpay_key": settings.RAZORPAY_KEY_ID,
                    "amount": int(total_price * 100), 
                    "order": {"total_price": total_price}, 
                },
            )

        return render(request, "quick_order.html", {"form": form})

    
    
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from decimal import Decimal

def payment_success(request):
    razorpay_order_id = request.session.get("razorpay_order_id")
    quick_order_data = request.session.get("quick_order_data")

    if not quick_order_data or not razorpay_order_id:
        return JsonResponse({"status": "error", "message": "Invalid session data!"})

    product = get_object_or_404(Product, id=quick_order_data["product_id"])

    total_price = Decimal(str(quick_order_data["total_price"]))

    quick_order = Quick_Order(
        customer=request.user,
        product=product,
        quantity=quick_order_data["quantity"],
        order_date=quick_order_data["order_date"],
        location_url=quick_order_data["location_url"],
        total_price=total_price, 
        is_paid=True,
    )
    quick_order.save()
    request.session.pop("quick_order_data", None)
    request.session.pop("razorpay_order_id", None)

    return JsonResponse({"status": "success", "message": "Payment successful!"})


class Bill_Order_View(View):
    def get(self, request, *args, **kwargs):
        data=Order.objects.filter(customer=request.user)
        return render(request,'bill_order.html',{'data':data})
    
class Bill_Quick_Order_View(View):
    def get(self, request, *args, **kwargs):
        data=Quick_Order.objects.filter(customer=request.user)
        return render(request,'bill_quick_order.html',{'data':data})
    
class All_Payments_View(View):
    def get(self,request):
        return render(request,'all_payments.html')

class All_Order_Payment_View(View):
    def get(self, request, *args, **kwargs):
        data = Order.objects.all().order_by('-id')

        # Pagination (5 orders per page)
        paginator = Paginator(data, 5)  
        page_number = request.GET.get('page')  
        page_obj = paginator.get_page(page_number)

        return render(request, 'all_order_payments.html', {'page_obj': page_obj})

    
class All_Quick_Payments_View(View):
    def get(self, request, *args, **kwargs):
        data = Quick_Order.objects.all().order_by('-id')

        # Pagination (5 orders per page)
        paginator = Paginator(data, 5)  
        page_number = request.GET.get('page')  
        page_obj = paginator.get_page(page_number)

        return render(request, 'all_quick_payments.html', {'page_obj': page_obj})
    
    
import random
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.cache import cache  # To store OTP temporarily
from .forms import ForgotPasswordForm,OTPVerificationForm,ResetPasswordForm

from .models import UserProfile_Model

def send_otp_email(username):
    try:
        user = User.objects.get(username=username)  # Fetch User object
        user_profile = UserProfile_Model.objects.get(user=user)  # Fetch associated profile
        
        if not user_profile.email:  # Ensure the user has an email
            return False  

        otp = random.randint(100000, 999999)  # Generate a 6-digit OTP
        cache.set(f"otp_{username}", otp, timeout=300)  # Store OTP for 5 minutes

        subject = "Password Reset OTP"
        message = f"Hello {username},\n\nYour OTP for password reset is: {otp}\n\nThis OTP is valid for 5 minutes."
        send_mail(subject, message, "your_email@example.com", [user_profile.email])  # Fetch email from UserProfile_Model
        return True  

    except User.DoesNotExist:
        return False
    except UserProfile_Model.DoesNotExist:
        return False


def forgot_password(request):
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email_sent = send_otp_email(username)

            if email_sent:
                request.session["reset_username"] = username  # Store username for next step
                return redirect("verify_otp")  # Redirect to OTP verification page
            else:
                messages.error(request, "No valid email associated with this account.")
    else:
        form = ForgotPasswordForm()
    
    return render(request, "forgot_password.html", {"form": form})



def verify_otp(request):
    if "reset_username" not in request.session:
        return redirect("forgot_password")  # Redirect if username is missing

    username = request.session["reset_username"]
    
    if request.method == "POST":
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            user_otp = form.cleaned_data["otp"]
            stored_otp = cache.get(f"otp_{username}")

            if stored_otp and str(stored_otp) == user_otp:
                cache.delete(f"otp_{username}")  # OTP used, remove it
                return redirect("reset_password")  # Redirect to reset password
            else:
                messages.error(request, "Invalid OTP or expired OTP!")
    else:
        form = OTPVerificationForm()
    
    return render(request, "verify_otp.html", {"form": form})

from django.contrib.auth.hashers import make_password

def reset_password(request):
    if "reset_username" not in request.session:
        return redirect("forgot_password")  # Redirect if session expired

    username = request.session["reset_username"]
    user = User.objects.get(username=username)

    if request.method == "POST":
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user.password = make_password(form.cleaned_data["new_password"])  # Hash the password
            user.save()
            del request.session["reset_username"]  # Remove session data
            messages.success(request, "Password reset successfully! You can now log in.")
            return redirect("login")  # Redirect to login page
    else:
        form = ResetPasswordForm()
    
    return render(request, "reset_password.html", {"form": form})
