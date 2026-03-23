from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.product_list, name='main'),
    path('about_page', views.about_page, name="about_page"),
    path('login_page', views.login_page, name="login_page"),
    path('reg_page', views.reg_page, name="reg_page"),
    path('contact', views.contact_page, name="contact"),
    path('category', views.category_page, name="category"),
    path('profile', views.profile_page, name="profile"), 
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('<slug:category_slug>/', views.product_list, name="product_list_by_category"),
    path('<int:id>/<slug:slug>', views.product_detail, name='product_detail'),
]