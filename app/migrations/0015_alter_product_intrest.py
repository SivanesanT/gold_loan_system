# Generated by Django 4.2.4 on 2023-10-14 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_product_transfer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='intrest',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='0-default', max_digits=8),
        ),
    ]
