# Generated by Django 3.2.5 on 2022-05-27 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='profile_pic',
            field=models.ImageField(blank=True, default='profile_pic.png', null=True, upload_to=''),
        ),
    ]
