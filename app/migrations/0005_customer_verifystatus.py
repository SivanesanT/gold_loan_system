# Generated by Django 4.2.4 on 2023-09-28 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_delete_regiverfy'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='verifystatus',
            field=models.BooleanField(default=False, help_text='0-default,1-true'),
        ),
    ]
