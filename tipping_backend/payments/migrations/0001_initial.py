# Generated by Django 5.1.4 on 2024-12-30 07:35

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
            name='PaymentHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transaction_id', models.CharField(max_length=255, unique=True)),
                ('status', models.CharField(choices=[('success', 'Success'), ('failed', 'Failed')], max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(blank=True, limit_choices_to={'role': 'customer'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payments', to=settings.AUTH_USER_MODEL)),
                ('staff', models.ForeignKey(limit_choices_to={'role': 'staff'}, on_delete=django.db.models.deletion.CASCADE, related_name='tips', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
