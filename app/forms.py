from django import forms


from app.models import User
from app.models import UserProfile_Model
from app.models import Product
from app.models import Order
from app.models import Quick_Order


class Product_Form(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['size', 'price', 'description']
        widgets = {
            'size': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter size (e.g., 1L, 2L)'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter price'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter product description',
                'rows': 4,
                'style': 'resize:none;'
            }),
        }




# class Registration_Form(forms.ModelForm):
#     class Meta:
#         model=User
#         fields=['username','password']

#         widgets={
#             'username':forms.TextInput(attrs={'class':'form-control',
#                                               'placeholder': 'Username . . .'}),
#             'password':forms.PasswordInput(attrs={'class':'form-control',
#                                                   'placeholder': 'Password . . .'})
#         }

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class Registration_Form(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username . . .',
            'id': 'username'
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password . . .',
            'id': 'password'
        })
    )
    
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password . . .',
            'id': 'confirm_password'
        })
    )
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists")
        return username
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        # Use Django's built-in password validators
        try:
            validate_password(password)
        except ValidationError as e:
            raise ValidationError(list(e.messages))
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords don't match")
        
        return cleaned_data
    
    def save(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        user = User.objects.create_user(
            username=username,
            password=password
        )
        return user

class UserProfile_Form(forms.ModelForm):
    class Meta:
        model=UserProfile_Model
        fields=['name','address','pincode','email','phone_number']
        read_only_fields=['user','created_date','updated_date','is_active']

        widgets={

            'name':forms.TextInput(attrs={'class':'form-control my-1',
                                          'placeholder': 'Enter your name . . .',
                                          'style':'background-color:rgba(255, 255, 255, 0.75);border:2px solid rgba(0, 0, 0, 0.1)'}),
            'address': forms.Textarea(attrs={'class': 'form-control my-1','placeholder': 'Enter your address . . .','rows': 2,
                                            'cols': 20, 'style': 'background-color:rgba(255, 255, 255, 0.75);'
                                            'border:2px solid rgba(0, 0, 0, 0.1); resize: none;'}),
            'pincode':forms.TextInput(attrs={'class':'form-control my-1',
                                          'placeholder': 'Enter your pincode . . .',
                                          'style':'background-color:rgba(255, 255, 255, 0.75);border:2px solid rgba(0, 0, 0, 0.1)'}),
            'email':forms.EmailInput(attrs={'class':'form-control my-1',
                                               'placeholder':'Enter your email . . .',
                                               'style':'background-color:rgba(255, 255, 255, 0.75);border:2px solid rgba(0, 0, 0, 0.1)'}),
            'phone_number':forms.NumberInput(attrs={'class':'form-control my-1',
                                            'placeholder':'Enter Your phone number . . .',
                                            'style':'background-color:rgba(255, 255, 255, 0.75);border:2px solid rgba(0, 0, 0, 0.1)'}),
        } 


class Login_Form(forms.Form):

    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control my-1',
            'placeholder': 'Username . . .',
            'style': 'background-color:rgba(255, 255, 255, 0.7)',
        })
    )
    
    password = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control my-1',
            'placeholder': 'Password . . .',
            'style': 'background-color:rgba(255, 255, 255, 0.7)',
        })
    )


class Order_Form(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['product', 'quantity', 'order_date']

        widgets = {
            'product': forms.Select(attrs={
                'class': 'form-control my-1',
                'style': 'background-color:rgba(255, 255, 255, 0.75); border:2px solid rgba(0, 0, 0, 0.1);',
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control my-1',
                'placeholder': 'Enter quantity . . .',
                'min': '1',
                'style': 'background-color:rgba(255, 255, 255, 0.75); border:2px solid rgba(0, 0, 0, 0.1);',
            }),
            'order_date': forms.DateInput(attrs={
                'class': 'form-control my-1',
                'type': 'date',
                'id': 'order_date',
                'style': 'background-color:rgba(255, 255, 255, 0.75); border:2px solid rgba(0, 0, 0, 0.1);',
            }),
        }


class Quick_Order_Form(forms.ModelForm):
    class Meta:
        model = Quick_Order
        fields = ['product', 'quantity', 'order_date', 'location_url']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'order_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control','id': 'order_date',}),
            'location_url': forms.TextInput(attrs={'id': 'location', 'class': 'form-control'}),
        }


from django import forms
from django.contrib.auth.models import User

class ForgotPasswordForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control my-1',
            'placeholder': 'Enter your username . . .',
            'style': 'background-color:rgba(255, 255, 255, 0.7)',
        })
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username does not exist.")
        return username


class OTPVerificationForm(forms.Form):
    otp = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-control my-1',
            'placeholder': 'Enter OTP . . .',
            'style': 'background-color:rgba(255, 255, 255, 0.7)',
        })
    )


class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control my-1',
            'placeholder': 'New Password . . .',
            'style': 'background-color:rgba(255, 255, 255, 0.7)',
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control my-1',
            'placeholder': 'Confirm Password . . .',
            'style': 'background-color:rgba(255, 255, 255, 0.7)',
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
