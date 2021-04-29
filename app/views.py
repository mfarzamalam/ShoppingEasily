from django.shortcuts import render
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import UserRegistrationForm
from django.contrib import messages

class HomeView(View):
    def get(self, request):
        mobile = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')
        
        context = {'mobiles':mobile, 'laptops':laptops}
        
        return render(request, 'app/home.html', context)

class product_detail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        context = {'p':product}

        return render(request, 'app/productdetail.html', context)

def add_to_cart(request):
 return render(request, 'app/addtocart.html')

def buy_now(request):
 return render(request, 'app/buynow.html')

def profile(request):
 return render(request, 'app/profile.html')

def address(request):
 return render(request, 'app/address.html')

def orders(request):
 return render(request, 'app/orders.html')

def change_password(request):
 return render(request, 'app/changepassword.html')


class mobile(View):
    def get(self, request, brand=''):
        if brand == 'samsung' or brand == 'iphone':
            mobile = Product.objects.filter(category='M').filter(brand__iexact=brand)
        elif brand == 'below-10000':
            mobile = Product.objects.filter(category='M').filter(discount_price__lte=10000)
        elif brand == 'above-10000':
            mobile = Product.objects.filter(category='M').filter(discount_price__gte=10000)
        else:
            mobile = Product.objects.filter(category='M')

        context = {'mobile':mobile}

        return render(request, 'app/mobile.html', context)


class customerregistration(View):
    def get(self, request):
        forms = UserRegistrationForm()
        context = {'forms':forms}

        return render(request, 'app/customerregistration.html', context)

    def post(self, request):
        forms = UserRegistrationForm(request.POST)
        if forms.is_valid():
            forms.save()
            messages.info(request, "Successfully Registerd!")
            forms = UserRegistrationForm()

        context = {'forms':forms}
        return render(request, 'app/customerregistration.html', context)


def checkout(request):
 return render(request, 'app/checkout.html')
