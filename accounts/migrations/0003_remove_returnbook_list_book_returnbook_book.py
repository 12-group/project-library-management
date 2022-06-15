# Generated by Django 4.0.1 on 2022-06-15 17:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_finereceipts_debt_finereceipts_debt_left_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='returnbook',
            name='list_book',
        ),
        migrations.AddField(
            model_name='returnbook',
            name='book',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.book'),
        ),
    ]
