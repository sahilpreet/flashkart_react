# Generated by Django 3.1 on 2020-09-09 13:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0008_customer_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='email',
        ),
    ]
