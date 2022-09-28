from django.db.models import Q
from django.http import Http404
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer, CategoryProductSerializer


class ProductList(APIView):
    #get all the product
    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    #post a product
    def post(self, request, format=None):
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
          

class ProductDetails(APIView):
    def get_object(self, category_slug, product_slug):
        try:
         return Product.objects.filter(category__slug = category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404

    #get the details using slug
    def get(self, request, category_slug, product_slug, format=None):
        product = self.get_object(category_slug, product_slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)  

    #patch the data
    def put(self, request, category_slug, product_slug):
        product = self.get_object(category_slug, product_slug)
        serializer = ProductSerializer(product, data = request.data, partial = True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN) 

    #delete data
    def delete(self, request, category_slug, product_slug):
        product = self.get_object(category_slug, product_slug)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    


#Category list
class CategoryList(APIView):
    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
            serializer = CategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


#Category list with product
class CategoryProductList(APIView):
    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategoryProductSerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
            serializer = CategoryProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

#Category and product details
class CategoryProductDetails(APIView):
    def get_object(self, category_slug):
        try:
         return Category.objects.get(slug=category_slug)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, category_slug, format=None):
        category = self.get_object(category_slug)
        serializer = CategoryProductSerializer(category)
        return Response(serializer.data) 

    def put(self, request, category_slug):
        category = self.get_object(category_slug)
        serializer = CategoryProductSerializer(category, data = request.data, partial = True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN) 

    def delete(self, request, category_slug):
        category = self.get_object(category_slug)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  

#Q search
@api_view(['POST'])
def search(request):
    query = request.data.get('query','')

    if query:
        products = Product.objects.filter(Q(name__icontains=query)| Q(description__icontains=query))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    else:
        return Response({'Product not found'})            