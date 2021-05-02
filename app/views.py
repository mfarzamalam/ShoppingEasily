from django.shortcuts import render, HttpResponseRedirect, redirect
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import UserRegistrationForm, UserProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class HomeView(View):
    def get(self, request):
        mobile = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')
        
        context = {'mobiles':mobile, 'laptops':laptops}
        
        return render(request, 'app/home.html', context)



class product_detail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        button = "add"

        if request.user.is_authenticated:
            user = request.user
            Carts = Cart.objects.filter(user=user)

            for cart in Carts:
                if pk == cart.product.id:
                    button = "already"
                    break
                else:
                    button = "add"

        context = {'p':product, 'button':button}

        return render(request, 'app/productdetail.html', context)


@method_decorator(login_required, name='dispatch')
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


@method_decorator(login_required, name='dispatch')
class address(View):
    def get(self, request):
        address = Customer.objects.filter(user=self.request.user)
        context = {'address':address}

        return render(request, 'app/address.html', context)

@method_decorator(login_required, name='dispatch')
def address_delete(request, pk):
    address = Customer.objects.get(pk=pk)
    address.delete()

    return HttpResponseRedirect('/address/')




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


@login_required
def add_to_cart(request):
    user = request.user
    p_id = request.GET.get('p_id')
    all_user_cart = Cart.objects.filter(user=user)

    product = Product.objects.get(id=p_id)
    Cart(user=user, product=product).save()

    return redirect('/show-cart')

@login_required
def show_cart(request):
    amount = 0.0
    shipping_amount = 150.0
    total_amount = 0.0
    total_amount_before = 0.0
    total_amount_after = 0.0

    if request.user.is_authenticated:
        user = request.user
        carts = Cart.objects.filter(user=user)

        for cart_amount in carts:
            amount = cart_amount.product.discount_price * cart_amount.quantity

            total_amount += amount

        total_amount_before = total_amount
        total_amount_after = total_amount_before + shipping_amount
        
    context = {'carts':carts, 'before':total_amount_before, 'after':total_amount_after, 'shipping':shipping_amount}

    return render(request, 'app/addtocart.html', context)

@login_required
def plus_cart(request, pk):
    carts = Cart.objects.filter(pk=pk).filter(user=request.user)

    for cart in carts:
        quantity = cart.quantity + 1
    
    carts = Cart.objects.filter(pk=pk).update(quantity=quantity)

    return redirect('/show-cart')

@login_required
def minus_cart(request, pk):
    carts = Cart.objects.filter(pk=pk).filter(user=request.user)

    for cart in carts:
        if cart.quantity > 1:
            quantity = cart.quantity - 1
        else:
            return redirect('/show-cart')
    
    carts = Cart.objects.filter(pk=pk).update(quantity=quantity)

    return redirect('/show-cart')

@login_required
def remove_cart(request, pk):
    carts = Cart.objects.filter(pk=pk).filter(user=request.user)
    carts.delete()

    return redirect('/show-cart')



@login_required
def checkout(request):
    user = request.user
    address = Customer.objects.filter(user=user)
    carts = Cart.objects.filter(user=user)

    context = {'address':address, 'carts':carts}

    return render(request, 'app/checkout.html', context)

@login_required
def buy_now(request):
    user = request.user
    customer_id = request.GET.get('customer_id')
    customer = Customer.objects.get(id=customer_id)
    carts = Cart.objects.filter(user=user)

    for cart in carts:
        OrderPlaced(user=user, customer=customer, product=cart.product, quantity=cart.quantity).save()
        cart.delete()

    return render(request, 'app/buynow.html')

@login_required
def orders(request):
    user = request.user
    orders = OrderPlaced.objects.filter(user=user)

    context = {'orders':orders}

    return render(request, 'app/orders.html', context)