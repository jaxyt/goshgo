# Generated by Django 3.0.5 on 2020-11-26 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='avatar.png', upload_to='avatars/'),
        ),
    ]