from app.models import Cart

def cart_count(request):
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user)
        count = carts.count()
    
        return {'count':count}
    else:
        return {'count':0}