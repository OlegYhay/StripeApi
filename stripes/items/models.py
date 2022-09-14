from django.db import models


# Create your models here.


class Items(models.Model):
    class CurrencyChoice(models.TextChoices):
        rub = 'rub',
        usd = 'usd',
        eur = 'eur',

    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.CharField(max_length=255, verbose_name='Описание')
    price = models.IntegerField(verbose_name='Цена')
    img = models.ImageField(upload_to='img/', verbose_name='Изображение', null=True, blank=True)
    currency = models.CharField(max_length=255, choices=CurrencyChoice.choices, default=CurrencyChoice.rub)

    def __str__(self):
        return f'{self.name} {self.price} {self.currency}'


class Order(models.Model):
    item = models.ManyToManyField(Items, related_name='items', verbose_name='состав')
    total = models.IntegerField(verbose_name='Итоговая стоимость', default=0)
    discount = models.ForeignKey('Discount', on_delete=models.SET_NULL, verbose_name='скидка', null=True, blank=True)
    tax = models.ForeignKey('Tax', on_delete=models.SET_NULL, verbose_name='налог', null=True, blank=True)

    def get_sale(self):
        '''Расчитать стоимость со скидкой'''
        price = int(self.total * (100 - self.total) / 100)
        return price


class Discount(models.Model):
    coupon = models.CharField(max_length=255, verbose_name='Наименование скидки')
    sale = models.IntegerField('Скидка в процентах', blank=True, default=1)

    def __str__(self):
        return f'{self.sale}%'


class Tax(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование налога')
    tax = models.IntegerField('Налог в процентах', blank=True, default=0)

    def __str__(self):
        return f'{self.tax}%'
