# Generated by Django 3.0.5 on 2021-01-14 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_auto_20201203_0619'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='page',
            options={'ordering': ('-created',)},
        ),
        migrations.AddField(
            model_name='page',
            name='pathpattern',
            field=models.TextField(blank=True, default=''),
        ),
    ]