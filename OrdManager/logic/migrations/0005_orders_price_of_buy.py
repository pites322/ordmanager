# Generated by Django 2.1.7 on 2019-05-21 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logic', '0004_auto_20190521_1402'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='price_of_buy',
            field=models.IntegerField(default=1),
        ),
    ]