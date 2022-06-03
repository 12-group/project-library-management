# Generated by Django 3.2.5 on 2022-06-03 02:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20220603_0854'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category_book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='pubYear',
            field=models.PositiveIntegerField(default=2022, validators=[django.core.validators.MaxValueValidator(2022), django.core.validators.MinValueValidator(1500)]),
        ),
        migrations.AlterField(
            model_name='book',
            name='amount',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
