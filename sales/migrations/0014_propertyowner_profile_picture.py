# Generated by Django 5.1.2 on 2024-10-16 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0013_propertyowner_is_married'),
    ]

    operations = [
        migrations.AddField(
            model_name='propertyowner',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics/', verbose_name='Foto de Perfil'),
        ),
    ]
