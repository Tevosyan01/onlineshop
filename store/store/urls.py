from django.urls import path
from store import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<slug:category_slug>/', views.category_detail, name='category_detail'),
    path('category/<slug:category_slug>/<slug:subcategory_slug>/', views.subcategory_detail, name='subcategory_detail'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)