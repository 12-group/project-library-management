# Generated by Django 3.2.5 on 2022-06-10 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_book_description_alter_book_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='reader',
            name='creator',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
