from django.shortcuts import render, get_object_or_404

from store.models import Category, SubCategory, Product


# Create your views here.


def home(request):
    categories = Category.objects.prefetch_related('subcategories').all()
    context = {'categories': categories}
    return render(request, 'store/base.html',context)


# Представление для отображения подкатегорий в категории
def category_detail(request, category_slug):
    # Получаем категорию по slug
    category = get_object_or_404(Category, slug=category_slug)
    # Получаем все подкатегории, связанные с категорией
    subcategories = category.subcategories.all()
    context = {
        'category': category,
        'subcategories': subcategories,
    }
    return render(request, 'store/product.html', context)

# Представление для отображения товаров в подкатегории
def subcategory_detail(request, category_slug, subcategory_slug):
    category = get_object_or_404(Category, slug=category_slug)
    subcategory = get_object_or_404(SubCategory, slug=subcategory_slug, category=category)
    products = Product.objects.filter(subcategory=subcategory)
    categories = Category.objects.prefetch_related('subcategories').all()

    context = {
        'category': category,
        'subcategory': subcategory,
        'products': products,  # добавляем товары в контекст
        'categories': categories,  # добавляем все категории в контекст, чтобы отображать их в шаблоне
    }
    return render(request, 'store/sub_category.html', context)
