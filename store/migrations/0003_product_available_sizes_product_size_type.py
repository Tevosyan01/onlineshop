# Generated by Django 4.2.1 on 2024-10-04 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='available_sizes',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='product',
            name='size_type',
            field=models.CharField(choices=[('Обувь', 'Обувь'), ('Джинсы', 'Джинсы'), ('Футболка', 'Футболка')], default='Футболка', max_length=50),
        ),
    ]
