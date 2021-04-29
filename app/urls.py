from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import UserLoginForm, UserPasswordChange

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('product-detail/<int:pk>', views.product_detail.as_view(), name='product-detail'),
    path('mobile/', views.mobile.as_view(), name='mobile'),
    path('mobile/<slug:brand>', views.mobile.as_view(), name='mobile-brand'),
    path('registration/', views.customerregistration.as_view(), name='customerregistration'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html', authentication_form=UserLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('changepassword/', auth_views.PasswordChangeView.as_view(template_name='app/changepassword.html', form_class=UserPasswordChange, success_url = '/changepasswordDone/'), name='changepassword'),
    path('changepasswordDone/', auth_views.PasswordChangeView.as_view(template_name='app/changepasswordDone.html'), name='changepasswordDone'),
    
    path('cart/', views.add_to_cart, name='add-to-cart'),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.profile, name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('checkout/', views.checkout, name='checkout'),
]   + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)