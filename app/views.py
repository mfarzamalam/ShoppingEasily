from django.shortcuts import render, HttpResponseRedirect
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import UserRegistrationForm, UserProfileForm
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


class profile(View):
    def get(self, request, pk=''):
        if pk == '':
            form = UserProfileForm()
            address = Customer.objects.filter(user=self.request.user)
            count = address.count()
            button = "Submit"
            context = {'form':form, 'button':button, 'count':count}
    
        else:
            single_data = Customer.objects.get(pk=pk)
            form = UserProfileForm(instance=single_data)
            button = "Update"
            context = {'form':form, 'button':button}

        return render(request, 'app/profile.html', context)

    def post(self, request, pk=''):
        if pk == "":
            form = UserProfileForm(request.POST)
            if form.is_valid():
                user = request.user
                name = form.cleaned_data['name']
                locality = form.cleaned_data['locality']
                city = form.cleaned_data['city']
                zipcode = form.cleaned_data['zipcode']
                state = form.cleaned_data['state']

                update = Customer(user=user, name=name, locality=locality, city=city, zipcode=zipcode, state=state)
                update.save()
        
                messages.info(request, 'Successfully Added!')
                form = UserProfileForm()
                button = "Submit"

        else:
            single_data = Customer.objects.get(pk=pk)
            form = UserProfileForm(request.POST, instance=single_data)
            if form.is_valid():
                form.save()
                messages.info(request, 'Successfully Updated!')
                button = "Update"

        context = {'form':form, 'button':button}

        return render(request, 'app/profile.html', context)


class address(View):
    def get(self, request):
        address = Customer.objects.filter(user=self.request.user)
        context = {'address':address}

        return render(request, 'app/address.html', context)

def address_delete(request, pk):
    address = Customer.objects.get(pk=pk)
    address.delete()

    return HttpResponseRedirect('/address/')


def orders(request):
 return render(request, 'app/orders.html')


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
