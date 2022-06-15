# Generated by Django 4.0.1 on 2022-06-15 14:25

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='finereceipts',
            name='debt',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='finereceipts',
            name='debt_left',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='pubYear',
            field=models.PositiveIntegerField(null=True, validators=[accounts.models.MyMaxValueValidator(2023), accounts.models.MyMinValueValidator(2014)]),
        ),
        migrations.AlterField(
            model_name='bookliquidation',
            name='reason',
            field=models.CharField(choices=[('lost', 'Mất'), ('damaged', 'Hư hỏng'), ('user_lost', 'Người dùng làm mất')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='birth',
            field=models.DateField(null=True),
        ),
    ]