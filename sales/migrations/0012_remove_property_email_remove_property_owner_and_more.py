# Generated by Django 5.1.2 on 2024-10-16 10:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0011_bid_counteroffer_bid_status_alter_bid_amount_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='email',
        ),
        migrations.RemoveField(
            model_name='property',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='property',
            name='owner_name',
        ),
        migrations.RemoveField(
            model_name='property',
            name='phone_number',
        ),
        migrations.AddField(
            model_name='property',
            name='dislikes',
            field=models.ManyToManyField(blank=True, related_name='property_dislikes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='property',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='property_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='PropertyOwner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255, verbose_name='Nome completo')),
                ('phone_number', models.CharField(default='(00) 00000-0000', max_length=15, verbose_name='Celular')),
                ('email', models.EmailField(default='default@example.com', max_length=254, verbose_name='E-mail')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='property',
            name='owners',
            field=models.ManyToManyField(related_name='properties', to='sales.propertyowner'),
        ),
    ]
