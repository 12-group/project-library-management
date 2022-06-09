# Generated by Django 4.0.1 on 2022-06-09 15:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='number_of_book_remain',
            field=models.PositiveIntegerField(default=1, null=True, validators=[django.core.validators.MaxValueValidator(models.PositiveIntegerField(default=1, null=True)), django.core.validators.MinValueValidator(models.PositiveIntegerField(default=1, null=True))]),
        ),
    ]
