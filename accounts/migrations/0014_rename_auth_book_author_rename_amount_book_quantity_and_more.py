# Generated by Django 4.0.1 on 2022-06-05 03:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_rename_category_book_bookcategory'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='auth',
            new_name='author',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='amount',
            new_name='quantity',
        ),
        migrations.RemoveField(
            model_name='book',
            name='inputDate',
        ),
        migrations.AddField(
            model_name='book',
            name='addDate',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='pubYear',
            field=models.PositiveIntegerField(default=2022, validators=[django.core.validators.MaxValueValidator(2023), django.core.validators.MinValueValidator(1500)]),
        ),
        migrations.AlterField(
            model_name='book',
            name='publisher',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
