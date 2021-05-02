from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import UserLoginForm, UserPasswordChange, UserPasswordResetForm, UserSetPasswordForm

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
    
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='app/password_reset.html', form_class=UserPasswordResetForm), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class=UserSetPasswordForm), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),

    path('profile/', views.profile.as_view(), name='profile'),
    path('profile/<int:pk>', views.profile.as_view(), name='profile-edit'),
    path('address/', views.address.as_view(), name='address'),
    path('address/<int:pk>', views.address_delete, name='address-delete'),

    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('show-cart/', views.show_cart, name='show-cart'),
    path('plus-cart/<int:pk>', views.plus_cart, name='plus-cart'),
    path('minus-cart/<int:pk>', views.minus_cart, name='minus-cart'),
    path('remove-cart/<int:pk>', views.remove_cart, name='remove-cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('buy/', views.buy_now, name='buy-now'),
    path('orders/', views.orders, name='orders'),

]   + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)