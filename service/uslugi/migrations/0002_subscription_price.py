# Generated by Django 4.2.7 on 2024-02-10 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uslugi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='price',
            field=models.PositiveIntegerField(default=0, verbose_name='Факстическая стоимость'),
        ),
    ]