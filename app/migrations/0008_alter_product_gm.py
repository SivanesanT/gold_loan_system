# Generated by Django 4.2.4 on 2023-10-01 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='gm',
            field=models.DecimalField(decimal_places=3, max_digits=8),
        ),
    ]
