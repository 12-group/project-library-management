# Generated by Django 4.0.1 on 2022-06-11 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_staff_position_alter_staff_service'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='service',
            field=models.CharField(choices=[('Librarian', 'Thủ thư'), ('Cashier', 'Thủ quỹ'), ('Stockkeeper', 'Thủ kho'), ('ManagerDeparment', 'Ban giám đốc')], max_length=200, null=True),
        ),
    ]
