# Generated by Django 2.1.7 on 2019-06-08 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logic', '0009_auto_20190608_1700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='price_of_buy',
            field=models.DecimalField(decimal_places=2, default=1.0, max_digits=6),
        ),
    ]