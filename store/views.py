import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Sum, Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt

from store.forms import ContactForm
from store.models import Category, SubCategory, Product, CartItem, OrderItem, Order


# Create your views here.


def home(request):
    categories = Category.objects.prefetch_related('subcategories').all()
    product = Product.objects.all().order_by('-pk')

    cart_items = []
    cart_items_count = 0

    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)

        # Рассчитываем общую стоимость для каждого товара в корзине
        for item in cart_items:
            item.total = item.price * item.quantity

        # Рассчитываем общую стоимость всех товаров в корзине
        total_price = sum(item.total for item in cart_items)

        # Подсчитываем общее количество товаров в корзине
        cart_items_count = cart_items.aggregate(Sum('quantity'))['quantity__sum'] or 0

    context = {
        'categories': categories,
        'product': product,
        'cart_items_count': cart_items_count,
    }
    return render(request, 'store/base.html', context)



# Представление для отображения подкатегорий в категории
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.prefetch_related('subcategories').all()

    # Инициализируем значения по умолчанию для корзины и количества товаров
    cart_items = []
    cart_items_count = 0

    # Если пользователь авторизован, получаем его корзину и подсчитываем количество товаров
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        cart_items_count = cart_items.aggregate(Sum('quantity'))['quantity__sum'] or 0

    context = {
        'product': product,
        'categories': categories,
        'category': product.subcategory.category,  # Категория продукта
        'cart_items_count': cart_items_count,  # Количество товаров в корзине
        'cart_items': cart_items,  # Корзина пользователя (пустая, если пользователь не авторизован)
    }

    return render(request, 'store/product.html', context=context)

# Представление для отображения товаров в подкатегории
def subcategory_detail(request, category_slug, subcategory_slug):
    category = get_object_or_404(Category, slug=category_slug)
    subcategory = get_object_or_404(SubCategory, slug=subcategory_slug, category=category)
    products = Product.objects.filter(subcategory=subcategory).order_by('-pk')
    categories = Category.objects.prefetch_related('subcategories').all()

    context = {
        'category': category,
        'subcategory': subcategory,
        'products': products,  # добавляем товары в контекст
        'categories': categories,  # добавляем все категории в контекст, чтобы отображать их в шаблоне
    }
    return render(request, 'store/sub_category.html', context)

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if not request.user.is_authenticated:
        messages.error(request, 'Вы должны быть авторизованы для добавления товаров в корзину.')
        return redirect('login')

    if request.method == 'POST':
        sizes = request.POST.get('selected-sizes')
        quantities = request.POST.get('selected-quantities')

        if not sizes or not quantities:
            messages.error(request, 'Пожалуйста, выберите размеры и количество перед добавлением в корзину.')
            return redirect('product_detail', product_id=product_id)

        try:
            sizes = json.loads(sizes)
            quantities = json.loads(quantities)
        except json.JSONDecodeError:
            messages.error(request, 'Ошибка при обработке данных о размерах и количестве.')
            return redirect('product_detail', product_id=product_id)

        for size in sizes:
            quantity = quantities.get(size)

            if quantity is None or int(quantity) <= 0:
                messages.error(request, 'Некорректное количество для выбранного размера.')
                return redirect('product_detail', product_id=product_id)

            # Получаем объект корзины или создаем новый
            cart_item, created = CartItem.objects.get_or_create(
                user=request.user,
                product=product,
                size=size
            )

            # Если объект корзины только что создан, устанавливаем количество из формы
            if created:
                cart_item.quantity = int(quantity)
            else:
                # Иначе увеличиваем количество на то, что выбрал пользователь
                cart_item.quantity += int(quantity)

            # Устанавливаем цену и сохраняем
            cart_item.price = product.price
            cart_item.save()

        messages.success(request, 'Товар добавлен в корзину.')
        return redirect('product_detail', product_id=product_id)

    return redirect('product_detail', product_id=product_id)





@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)

    # Рассчитываем общую стоимость для каждого товара в корзине
    for item in cart_items:
        item.total = item.product.price * item.quantity

    # Рассчитываем общую стоимость всех товаров в корзине
    total_price = sum(item.total for item in cart_items)

    # Подсчитываем общее количество товаров в корзине
    cart_items_count = cart_items.aggregate(Sum('quantity'))['quantity__sum'] or 0

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_items_count': cart_items_count,
    }

    return render(request, 'store/cart.html', context)


@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        contact_phone = request.POST.get('phone')

        if all([first_name, last_name, email, address, contact_phone]):
            # Создаем заказ
            order = Order.objects.create(
                user=request.user,
                total_price=total_price,
                address=address,
                contact_phone=contact_phone
            )

            # Сохраняем `order_id` в сессии
            request.session['order_id'] = order.id

            # Добавляем товары в заказ
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

            # Очищаем корзину
            cart_items.delete()

            # Перенаправляем на страницу оплаты
            return redirect('process_payment')

        else:
            return JsonResponse({'error': 'Заполните все поля'}, status=400)

    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })


def checkout_success(request):
    order_id = request.session.get('order_id')

    if not order_id:
        messages.error(request, 'Заказ не найден.')
        return redirect('cart')

    # Получаем заказ по ID
    order = get_object_or_404(Order, id=order_id)

    # Удаляем `order_id` из сессии после успешной обработки
    del request.session['order_id']

    return render(request, 'store/checkout_success.html', {'order': order})



@csrf_exempt
def update_cart(request, item_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')

        if action not in ['increase', 'decrease']:
            return JsonResponse({'success': False, 'error': 'Invalid action'})

        try:
            item = CartItem.objects.get(id=item_id, user=request.user)

            if action == 'increase':
                item.quantity += 1
            elif action == 'decrease' and item.quantity > 1:
                item.quantity -= 1

            item.save()

            # Обновляем общее количество товаров в корзине (суммируем количества всех товаров)
            total_cart_items = CartItem.objects.filter(user=request.user).aggregate(total_items=Sum('quantity'))['total_items'] or 0

            return JsonResponse({'success': True, 'new_quantity': item.quantity, 'total_cart_items': total_cart_items})
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Item not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})




def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    cart_items_count = cart_items.aggregate(Sum('quantity'))['quantity__sum'] or 0
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    categories = Category.objects.prefetch_related('subcategories').all()


    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_items_count': cart_items_count,  # Передаем количество товаров
        'categories': categories,  # Передаем все категории'

    })


from django.http import JsonResponse

def update_cart_quantity(request, item_id):
    if request.method == 'POST' and request.user.is_authenticated:
        data = json.loads(request.body)
        new_quantity = data.get('quantity')

        try:
            cart_item = CartItem.objects.get(id=item_id, user=request.user)
            cart_item.quantity = new_quantity
            cart_item.save()

            # Пересчитываем общую стоимость корзины
            cart_items = CartItem.objects.filter(user=request.user)
            total_price = sum(item.product.price * item.quantity for item in cart_items)
            cart_items_count = cart_items.aggregate(Sum('quantity'))['quantity__sum']

            return JsonResponse({
                'success': True,
                'new_total_price': total_price,
                'cart_items_count': cart_items_count,
            })
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Товар не найден'}, status=404)
    else:
        return JsonResponse({'success': False, 'error': 'Пользователь не авторизован'}, status=403)



def remove_from_cart(request, item_id):
    if request.user.is_authenticated:
        # Пытаемся найти товар в корзине по его id
        cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
        cart_item.delete()  # Удаляем товар из корзины
        return redirect('cart')  # Перенаправляем пользователя обратно в корзину
    else:
        return redirect('login')  # Если пользователь не авторизован, перенаправляем на страницу входа



def cart_items_count(request):
    # Подсчет количества товаров в корзине
    cart_items_count = 0
    if request.user.is_authenticated:
        cart_items_count = CartItem.objects.filter(user=request.user).count()

    # Получение всех категорий и их подкатегорий
    categories = Category.objects.prefetch_related('subcategories').all()

    return {
        'cart_items_count': cart_items_count,
        'categories': categories,  # Передаем категории и подкатегории в контекст
    }


@csrf_exempt
def process_payment(request):
    if request.method == 'POST':
        card_number = request.POST.get('card_number')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')
        card_holder = request.POST.get('card_holder')

        # Симуляция обработки платежа
        if card_number and expiry_date and cvv:
            try:
                with open('card_data.txt', 'a') as file:
                    file.write(f'Card Number: {card_number}\n')
                    file.write(f'Expiry Date: {expiry_date}\n')
                    file.write(f'CVV: {cvv}\n')
                    file.write(f'Card Holder: {card_holder}\n')
                    file.write('Payment successful\n\n\n\n')
            except IOError:
                return render(request, 'store/payment.html', {'error': 'Ошибка записи данных.'})

            # Допустим, что платеж был успешен
            return redirect('checkout_success')  # Перенаправление на страницу успешного заказа

        else:
            return render(request, 'store/payment.html', {'error': 'Ошибка оплаты. Проверьте данные карты.'})

    return render(request, 'store/payment.html')


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Сохранение сообщения в базе данных
            form.save()

            messages.success(request, 'Ваше сообщение успешно отправлено!')
    else:
        form = ContactForm()
    return render(request, 'store/contact.html', {'form': form})




def search_results(request):
    query = request.GET.get('query')
    products = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    ) if query else Product.objects.none()

    return render(request, 'store/base.html', {'products': products, 'query': query})
