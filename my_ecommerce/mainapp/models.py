from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

User = get_user_model()

#************
#1 Category
# Product
# Cartproduct
#4 Cart
#5 Order
#************
#6 Customer
#7 Specification


class Category(models.Model):

    name = models.CharField(max_length=255, verbose_name='Категория', blank=False)
    slug = models.SlugField(unique=True, blank=False)


    # class Meta:
    #     ordering = ('name',)
    #     verbose_name = 'категория'
    #     verbose_name_plural = 'категории'


    # def get_url(self):
    #     return reverse('products_by_category', args=[self.slug])


    def __str__(self):
        return self.name


class Product(models.Model):

    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Наименование', unique=True, blank=False)
    slug = models.SlugField(unique=True, blank=False)
    image = models.ImageField(upload_to='product', blank=False, verbose_name="Изображение")
    description = models.TextField(blank=True, default='Мы работаем над этим', verbose_name="Описание")
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Цена")


    # class Meta:
    #     ordering = ('name',)
    #     verbose_name = 'продукт'
    #     verbose_name_plural = 'продукты'


    # def get_url(self):
    #     return reverse('products_by_category', args=[self.slug])


    def __str__(self):
        return self.title


class CartProduct(models.Model):

    user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart',verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
    product = models.ForeignKey(Product,verbose_name='Товар', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Общая стоимость")

    def __str__(self):
        return (f'Продукт: {self.product.title} (для корзины)')

class Cart(models.Model):

    owner = models.ForeignKey('Customer', verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0, unique=True)
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Общая стоимость")

    def __str__(self):
        return str(self.id)

class Customer(models.Model):

    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name="Номер телефона")
    address = models.CharField(max_length=255, verbose_name="Адрес")

    def __str__(self):
        return (f'Покупатель: {self.user.first_name} {self.user.last_name}')

class Specifications(models.Model):

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    name = models.CharField(max_length=255, verbose_name='Наименование товара для хараетеристик')

    def __str__(self):
        return (f'Характеристики товара: {self.name}')
