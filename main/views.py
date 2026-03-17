from django.shortcuts import render, get_object_or_404
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

def category_page(request):
    """Страница со всеми категориями"""
    categories = Category.objects.all()
    return render(request, "main/product/category_list.html", {  
        'categories': categories
    })