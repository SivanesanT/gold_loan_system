# Generated by Django 4.2.4 on 2023-10-01 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_alter_product_releasedate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='releasedate',
            field=models.DateField(null=True),
        ),
    ]
