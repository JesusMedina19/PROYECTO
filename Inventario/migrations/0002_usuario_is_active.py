# Generated by Django 5.1.3 on 2024-11-26 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventario', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
