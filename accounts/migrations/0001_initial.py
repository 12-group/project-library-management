# Generated by Django 3.2.5 on 2022-06-14 00:50

import accounts.initial_func
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BookCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('birth', models.DateField(blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('profile_pic', models.ImageField(blank=True, default='profile_pic.png', null=True, upload_to='')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reader',
            fields=[
                ('customer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='accounts.customer')),
                ('reader_type', models.CharField(blank=True, choices=[('Male', 'Nam'), ('Female', 'Nữ')], max_length=200, null=True)),
                ('email', models.EmailField(blank=True, max_length=200, null=True)),
                ('rId', models.CharField(default=accounts.initial_func.pk_gen, editable=False, max_length=255, primary_key=True, serialize=False, unique=True)),
                ('total_debt', models.PositiveIntegerField(default=0, null=True)),
            ],
            bases=('accounts.customer',),
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('customer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='accounts.customer')),
                ('certificate', models.CharField(blank=True, choices=[('Baccalaureate', 'Tú tài'), ('Intermediate', 'Trung cấp'), ('College1', 'Cao đẳng'), ('College2', 'Đại học'), ('Master', 'Thạc sĩ'), ('Doctor', 'Tiến sĩ')], max_length=200, null=True)),
                ('position', models.CharField(choices=[('President', 'Giám đốc'), ('Vice President', 'Phó giám đốc'), ('Manager', 'Trưởng phòng'), ('Deputy', 'Phó phòng'), ('Staff', 'Nhân viên')], max_length=200, null=True)),
                ('service', models.CharField(choices=[('Librarian', 'Thủ thư'), ('Cashier', 'Thủ quỹ'), ('Stockkeeper', 'Thủ kho'), ('Manager department', 'Ban giám đốc')], max_length=200, null=True)),
                ('sId', models.CharField(default=accounts.initial_func.staff_pk_gen, editable=False, max_length=255, primary_key=True, serialize=False, unique=True)),
                ('force_password_change', models.BooleanField(default=True)),
            ],
            bases=('accounts.customer',),
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('bId', models.CharField(default=accounts.initial_func.book_pk_gen, editable=False, max_length=255, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200, null=True)),
                ('cover_pic', models.ImageField(blank=True, default='logo.png', null=True, upload_to='')),
                ('author', models.CharField(blank=True, max_length=200, null=True)),
                ('price', models.PositiveIntegerField(default=0, null=True)),
                ('publisher', models.CharField(blank=True, max_length=200, null=True)),
                ('pubYear', models.PositiveIntegerField(default=2022, validators=[django.core.validators.MaxValueValidator(2023), django.core.validators.MinValueValidator(1500)])),
                ('addDate', models.DateTimeField(auto_now_add=True, null=True)),
                ('total', models.PositiveIntegerField(default=1, null=True)),
                ('number_of_book_remain', models.PositiveIntegerField(default=1, null=True)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('ctg', models.ManyToManyField(blank=True, to='accounts.BookCategory')),
                ('nguoinhan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.staff')),
            ],
        ),
        migrations.CreateModel(
            name='ReturnBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_return', models.DateTimeField(auto_now_add=True, null=True)),
                ('fine', models.PositiveIntegerField(default=0, null=True)),
                ('book', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.book')),
                ('reader', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.reader')),
            ],
        ),
        migrations.AddField(
            model_name='reader',
            name='card_maker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.staff'),
        ),
        migrations.CreateModel(
            name='PenaltyTicket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(blank=True, max_length=200, null=True)),
                ('fine', models.PositiveIntegerField(default=0, null=True)),
                ('reader', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.reader')),
                ('staff', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.staff')),
            ],
        ),
        migrations.CreateModel(
            name='GetBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0, null=True)),
                ('get_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('book', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.book')),
                ('staff', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.staff')),
            ],
        ),
        migrations.CreateModel(
            name='FineReceipts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proceeds', models.PositiveIntegerField(default=0, null=True)),
                ('date_pay_fine', models.DateTimeField(auto_now_add=True, null=True)),
                ('reader', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.reader')),
                ('staff', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.staff')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.book')),
                ('reader', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.reader')),
            ],
        ),
        migrations.CreateModel(
            name='BorrowOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, choices=[('Pending ', 'Chờ xác nhận'), ('Inprocess', 'Đang soạn sách'), ('Complete', 'Hoàn thành')], default='Chờ xác nhận', max_length=200, null=True)),
                ('book', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.book')),
                ('reader', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.reader')),
            ],
        ),
        migrations.CreateModel(
            name='BorrowBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_borrow', models.DateTimeField(auto_now_add=True, null=True)),
                ('book', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.book')),
                ('reader', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.reader')),
            ],
        ),
        migrations.CreateModel(
            name='BookLiquidation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0, null=True)),
                ('reason', models.CharField(blank=True, max_length=200, null=True)),
                ('date_liquidation', models.DateTimeField(auto_now_add=True, null=True)),
                ('book', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.book')),
                ('staff', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.staff')),
            ],
        ),
    ]
