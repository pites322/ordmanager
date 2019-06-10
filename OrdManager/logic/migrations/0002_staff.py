# Generated by Django 2.1.7 on 2019-05-11 13:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('logic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=80, verbose_name='Фамилия')),
                ('first_name', models.CharField(max_length=80, verbose_name='Имя')),
                ('second_name', models.CharField(blank=True, max_length=80, null=True, verbose_name='Отчество')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]