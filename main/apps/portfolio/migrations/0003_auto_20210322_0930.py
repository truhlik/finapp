# Generated by Django 3.1.4 on 2021-03-22 09:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20210311_1046'),
        ('portfolio', '0002_auto_20210311_1046'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolio',
            name='evaluation',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='portfolio', to='products.product'),
        ),
    ]
