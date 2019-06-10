# Generated by Django 2.1.7 on 2019-05-20 15:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('logic', '0002_staff'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buyId', models.CharField(max_length=80)),
                ('name', models.CharField(max_length=80)),
                ('data', models.DateField(auto_now=True)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='logic.Staff')),
            ],
        ),
    ]
