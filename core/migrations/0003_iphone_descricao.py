# Generated by Django 5.0.6 on 2024-06-07 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_iphone'),
    ]

    operations = [
        migrations.AddField(
            model_name='iphone',
            name='descricao',
            field=models.TextField(blank=True, max_length=400),
        ),
    ]
