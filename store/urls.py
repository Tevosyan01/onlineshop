from django.urls import path, include
from store import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('category/<slug:category_slug>/<slug:subcategory_slug>/', views.subcategory_detail, name='subcategory_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),  # URL для страницы корзины
    path('users/', include('django.contrib.auth.urls')),
    path('checkout/', views.checkout, name='checkout'),  # Добавляем URL для оформления покупки
    path('checkout_success/', views.checkout_success, name='checkout_success'),
    path('update-cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('payment/', views.process_payment, name='process_payment'),
    path('contact', views.contact_view, name='contact'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)