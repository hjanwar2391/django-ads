# Generated by Django 5.0.6 on 2024-09-15 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads_app', '0006_withdrawal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='withdrawal',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('processing', 'Processing'), ('completed', 'Completed'), ('canceled', 'Canceled')], default='pending', max_length=10),
        ),
    ]
