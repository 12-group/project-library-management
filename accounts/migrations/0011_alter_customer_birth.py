# Generated by Django 4.0.1 on 2022-06-05 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_rename_category_reader_categoryreader'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='birth',
            field=models.DateField(null=True),
        ),
    ]
