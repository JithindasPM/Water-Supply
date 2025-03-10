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




class Registration_Form(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','password']

        widgets={
            'username':forms.TextInput(attrs={'class':'form-control',
                                              'placeholder': 'Username . . .'}),
            'password':forms.PasswordInput(attrs={'class':'form-control',
                                                  'placeholder': 'Password . . .'})
        }

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
            'order_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'location_url': forms.TextInput(attrs={'id': 'location', 'class': 'form-control'}),
        }
