# Generated by Django 4.1.1 on 2022-09-13 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0004_alter_items_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='discount',
            old_name='name',
            new_name='coupon',
        ),
        migrations.AlterField(
            model_name='order',
            name='total',
            field=models.IntegerField(default=0, verbose_name='Итоговая стоимость'),
        ),
    ]
