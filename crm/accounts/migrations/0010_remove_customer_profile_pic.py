# Generated by Django 5.0.7 on 2024-08-09 04:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_customer_profile_pic_alter_order_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='profile_pic',
        ),
    ]
