# Generated by Django 4.0.1 on 2022-06-09 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_book_number_of_book_remain'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]