# Generated by Django 3.1.4 on 2021-03-11 10:46

from django.db import migrations, models


def change_values(apps, schema):
    Product = apps.get_model('products.Product')
    for p in Product.objects.all():
        p.evaluation = p.evaluation / 10000
        p.save()


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20210305_1333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='evaluation',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.RunPython(change_values)
    ]