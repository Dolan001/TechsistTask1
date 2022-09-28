from django.urls import path, include
from . import views

urlpatterns = [
    path('products/', views.ProductList.as_view()),
    path('products/<slug:category_slug>/<slug:product_slug>/', views.ProductDetails.as_view()),

    path('categories/', views.CategoryList.as_view()),
    path('category-product-list/', views.CategoryProductList.as_view()),
    path('category-product-list/<slug:category_slug>/', views.CategoryProductDetails.as_view()),

    path('products/search/', views.search),
]