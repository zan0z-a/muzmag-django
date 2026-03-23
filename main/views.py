from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Category, Product

def product_list(request, category_slug=None):
    categories = Category.objects.all()  
    products = Product.objects.filter(available=True)
    category = None
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        template_name = 'main/product/category_products.html'  
    else:
        template_name = 'main/product/list.html' 
    
    return render(request, template_name, {
        'category': category,
        'categories': categories,  
        'products': products
    })

def product_detail(request, id, slug):
    categories = Category.objects.all()  
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    related_products = Product.objects.filter(
        category=product.category, 
        available=True
    ).exclude(id=product.id)[:4]
    
    return render(request, 'main/product/detail.html', {
        'product': product, 
        'related_products': related_products,
        'categories': categories 
    })

def about_page(request):
    return render(request, "main/public/about.html")

def login_page(request):
    return render(request, "main/public/login.html")

def reg_page(request):
    return render(request, "main/public/reg.html")

def contact_page(request):
    return render(request, "main/public/contact.html")

def cart_page(request):
    return render(request, "main/public/cart.html")

def category_page(request):
    """Страница со всеми категориями"""
    categories = Category.objects.all()
    return render(request, "main/product/category_list.html", {  
        'categories': categories
    })

def login_page(request):
    """Страница входа"""
    return render(request, "main/public/login.html")

def reg_page(request):
    """Страница регистрации"""
    return render(request, "main/public/reg.html")

def login_view(request):
    """Обработка входа по email"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Ищем пользователя по email
        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            messages.error(request, 'Пользователь с таким email не найден')
            return redirect('main:login_page')
        
        # Аутентификация по username
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Добро пожаловать!')
            return redirect('main:main')
        else:
            messages.error(request, 'Неверный email или пароль')
            return redirect('main:login_page')
    
    return redirect('main:login_page')

def register_view(request):
    """Обработка регистрации"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Проверка на пустые поля
        if not username or not email or not password1 or not password2:
            messages.error(request, 'Все поля обязательны для заполнения')
            return redirect('main:reg_page')
        
        # Проверка совпадения паролей
        if password1 != password2:
            messages.error(request, 'Пароли не совпадают')
            return redirect('main:reg_page')
        
        # Проверка длины пароля
        if len(password1) < 6:
            messages.error(request, 'Пароль должен быть не менее 6 символов')
            return redirect('main:reg_page')
        
        # Проверка существования пользователя
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует')
            return redirect('main:reg_page')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с таким email уже существует')
            return redirect('main:reg_page')
        
        # Создание пользователя
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        
        messages.success(request, f'Регистрация прошла успешно! Теперь вы можете войти.')
        return redirect('main:login_page')
    
    return redirect('main:reg_page')

def logout_view(request):
    """Выход из аккаунта"""
    logout(request)
    messages.success(request, 'Вы вышли из аккаунта')
    return redirect('main:main')

def profile_page(request):
    """Страница профиля пользователя"""
    return render(request, "main/public/profile.html")