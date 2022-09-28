from django.db import models

#category model
class Category(models.Model):
    name = models.CharField(max_length=150)
    img = models.ImageField(upload_to='uploads/categories/', blank=True, null = True)
    slug = models.SlugField(unique=True)

    #ordering data by names
    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name    

    #get the absolute url
    def get_category_url(self):
        return f'/{self.slug}/'

    #make img url
    def get_img(self):
        if self.img:
            return 'http://127.0.0.1:8000' + self.img.url  
        return ""      

#product model
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    img = models.ImageField(upload_to='uploads/products/', blank=True, null = True)
    date_time = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ('-date_time',)

    def __str__(self):
        return self.name 

    def get_product_url(self):
        return f'/{self.category.slug}/{self.slug}'

    def get_img(self):
        if self.img:
            return 'http://127.0.0.1:8000' + self.img.url  
        return ""             
