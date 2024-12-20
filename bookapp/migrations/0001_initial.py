# Generated by Django 5.1.1 on 2024-12-01 00:33

import bookapp.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=200)),
                ('isbn', models.PositiveIntegerField()),
                ('category', models.CharField(choices=[('Fiction', 'Fiction'), ('Non-Fiction', 'Non-Fiction'), ('Science', 'Science'), ('Biography', 'Biography'), ('Poetry', 'Poetry'), ('Education', 'Education')], max_length=50)),
                ('pdf_file', models.FileField(blank=True, null=True, upload_to='book_pdfs/')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classroom', models.CharField(max_length=10)),
                ('branch', models.CharField(max_length=10)),
                ('roll_no', models.CharField(max_length=3, unique=True)),
                ('phone', models.CharField(blank=True, max_length=10)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='IssuedBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issued_date', models.DateField(auto_now_add=True)),
                ('expiry_date', models.DateField(default=bookapp.models.get_expiry_date)),
                ('book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bookapp.book')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='issued_books', to='bookapp.student')),
            ],
        ),
    ]
