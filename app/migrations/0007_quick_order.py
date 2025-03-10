# Generated by Django 5.0.3 on 2025-03-09 10:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_order_status'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Quick_Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('total_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('order_date', models.DateField()),
                ('created_date', models.DateField(auto_now_add=True, null=True)),
                ('status', models.CharField(choices=[('Requested', 'Requested'), ('Pending', 'Pending'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], default='Requested', max_length=20)),
                ('location_url', models.URLField(blank=True, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.product')),
            ],
        ),
    ]
